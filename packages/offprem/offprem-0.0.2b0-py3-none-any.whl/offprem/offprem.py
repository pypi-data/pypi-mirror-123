from configparser import DuplicateSectionError
from typing import Optional, Any, Iterator
from dataclasses import dataclass, field
from pathlib import Path
import logging
import json

import boto3
from parserconfig import ParserConfig
from botocore.exceptions import ClientError


@dataclass
class VirtualPrivateCloud:
    """ Attributes for an AWS VPC. """
    id: str
    name: str
    region: str


@dataclass
class Profile:
    """ Attributes for an AWS Profile. """
    profile_name: str = field(default=None)
    source_profile: Optional[str] = field(default=None)
    role_arn: Optional[str] = field(default=None)
    mfa_serial: Optional[str] = field(default=None)


@dataclass
class ConfigureCredentials(ParserConfig):
    """ Retrieve AWS credentials from a configuration file. """
    configuration_file: Path = field(default=Path.home().joinpath('.aws/credentials'))

    def query(self, profile_name: str) -> Profile:
        """ Retrieve credential settings from `self.configuration_file`. """
        source_profile = self.configuration_file_parser.get(section=profile_name, option='source_profile', fallback=None)
        role_arn = self.configuration_file_parser.get(section=profile_name, option='role_arn', fallback=None)
        mfa_serial = self.configuration_file_parser.get(section=source_profile or profile_name,
                                                        option='mfa_serial', fallback=None)

        return Profile(profile_name=profile_name, source_profile=source_profile, role_arn=role_arn,
                       mfa_serial=mfa_serial)

    def sts(self, profile_name: str) -> 'SecurityTokenService':
        """ Retrieve temporary credentials from the Security Token Service. """
        profile = self.query(profile_name=profile_name)
        sts = SecurityTokenService(profile=profile)
        return sts


@dataclass
class ConfigureVPC(ParserConfig):
    """ Set and retrieve VPC ID's and regions in a configuration file. """
    configuration_file: Path = field(default=Path.home().joinpath('.aws/environments.ini'))
    create_configuration_file: bool = field(default=True, repr=False)

    def query(self, vpc_name: str) -> VirtualPrivateCloud:
        """ Retrieve VPC settings from `self.configuration_file`. """
        vpc_id = self.configuration_file_parser.get(section=vpc_name, option='vpc_id')
        region_name = self.configuration_file_parser.get(section=vpc_name, option='region_name')
        return VirtualPrivateCloud(id=vpc_id, name=vpc_name, region=region_name)

    def populate_configuration_file(self, vpc_id: str, name: str, region: str, tags: Optional[str]) -> None:
        """ Add a single VPC to `self.configuration_file`. """
        try:
            logging.info(msg=f'{name = }')
            self.configuration_file_parser.add_section(section=name)
        except DuplicateSectionError:
            pass  # Every section is uniquely named with its VPC ID and region.
        finally:
            self.configuration_file_parser[name]['vpc_id'] = vpc_id
            self.configuration_file_parser[name]['region_name'] = region
            if tags:
                self.configuration_file_parser[name]['tags'] = tags


@dataclass
class AWSPremise:
    """ Authenticated boto3 session and VPC attributes. """
    vpc: VirtualPrivateCloud = field(init=False, default=None)
    session: boto3.session = field(init=False, default=None)
    vpc_configuration: ConfigureVPC = field(default_factory=ConfigureVPC)
    session_configuration: ConfigureCredentials = field(default_factory=ConfigureCredentials)

    def assign(self, profile_name: str, vpc_name: Optional[str] = None) -> None:
        """ Populate the boto3 session with STS credentials and assign the vpc variable if vpc_name is given. """
        sts = self.session_configuration.sts(profile_name=profile_name)

        if vpc_name:
            self.vpc = self.vpc_configuration.query(vpc_name=vpc_name)
            self.session = boto3.session.Session(**sts.credentials, profile_name=profile_name, region_name=self.vpc.region)
        else:
            self.session = boto3.session.Session(**sts.credentials, profile_name=profile_name)

    @staticmethod
    def search_vpc_tags(vpc: Any, search_tags: Iterator) -> str:
        """ Return the name of the VPC. """
        if vpc.tags:
            for tag in vpc.tags:
                if tag.get('Key') in search_tags:
                    return tag['Value'].lower()

    @staticmethod
    def reformat_vpc_tags(vpc: boto3) -> Optional[str]:
        """ Flatten the list of dicts into one dict and convert the dict object to a string. """
        extract_tag_values = {tag['Key']: tag['Value'] for tag in vpc.tags}
        tags = json.dumps(obj=extract_tag_values) if extract_tag_values else None
        return tags

    def get_all_vpcs(self, search_tags: Optional[Iterator] = None, empty_tags: bool = False) -> None:
        """ Gather existing VPCs in every available region. """
        assert any([search_tags, empty_tags]), 'get_all_vpcs requires either search_tags or empty_tags to be set.'

        for region in self.session.get_available_regions(service_name='ec2'):
            try:
                for vpc in self.session.resource(service_name='ec2', region_name=region).vpcs.all():
                    if found_tag := self.search_vpc_tags(vpc=vpc, search_tags=search_tags) if search_tags else None:
                        name = f'{found_tag}|{vpc.id}|{region}'
                    elif not found_tag and empty_tags:
                        name = f'{vpc.id}|{region}'
                    else:
                        # The else clause is met when `found_tag` is not defined and `empty_tags` is set to False.
                        # Move on to the next VPC in the `vpc` variable.
                        continue

                    tags = self.reformat_vpc_tags(vpc=vpc)
                    self.vpc_configuration.populate_configuration_file(vpc_id=vpc.id, name=name, region=region, tags=tags)

            except ClientError:
                # When no VPCs exist in a region, `ClientError` is raised. We pass this exception to move on to the
                # next region. Unfortunately, there are many conditions where `ClientError` can be raised, so a
                # potential issue could be masked.
                pass

        # Only save the configuration file if no unhandled exceptions occur.
        self.vpc_configuration.save_configuration_file()


@dataclass
class SecurityTokenService:
    """ Generate temporary credentials. """
    profile: Profile
    credentials: dict = field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        """ Differentiate between user and role for temporary credentials. """
        if all([self.profile.source_profile, self.profile.role_arn]):
            self.generate_role_credentials()
        else:
            self.generate_user_credentials()

    def request_mfa_token(self) -> str:
        """ Request an MFA token. """
        return input(f'Enter the MFA Token for {self.profile.mfa_serial}: ')

    def rename_sts_credentials(self, credentials: dict) -> dict:
        """ Rename keys for credentials received by the Security Token Service. """
        # This is done to support kwargs unpacking into `boto3.session.Session` objects.
        self.credentials['aws_access_key_id'] = credentials['Credentials']['AccessKeyId']
        self.credentials['aws_secret_access_key'] = credentials['Credentials']['SecretAccessKey']
        self.credentials['aws_session_token'] = credentials['Credentials']['SessionToken']
        return self.credentials

    def generate_user_credentials(self) -> dict:
        """ Generate temporary credentials for an IAM user. """
        client_sts = boto3.session.Session(profile_name=self.profile.profile_name).client('sts')

        if self.profile.mfa_serial:
            credentials = client_sts.get_session_token(SerialNumber=self.profile.mfa_serial,
                                                       TokenCode=self.request_mfa_token())
        else:
            credentials = client_sts.get_session_token()

        return self.rename_sts_credentials(credentials=credentials)

    def generate_role_credentials(self) -> dict:
        """ Generate temporary credentials for an IAM role. """
        client_sts = boto3.session.Session(profile_name=self.profile.source_profile).client('sts')

        if self.profile.mfa_serial:
            credentials = client_sts.assume_role(RoleArn=self.profile.role_arn,
                                                 RoleSessionName='AssumeRole',
                                                 SerialNumber=self.profile.mfa_serial,
                                                 TokenCode=self.request_mfa_token())
        else:
            credentials = client_sts.assume_role(RoleArn=self.profile.role_arn,
                                                 RoleSessionName='AssumeRole')

        return self.rename_sts_credentials(credentials=credentials)
