import logging

import boto3

from offprem.offprem import ConfigureVPC


def select_profile():
    return input(f'Select a profile: {boto3.session.Session().available_profiles}\n')


def select_vpc():
    return input(f'Select a VPC:\n{ConfigureVPC.configuration_file_parser.sections()}\n')


logging.basicConfig(format='{name} - {levelname} - {message}', level=logging.INFO, style='{')
logger = logging.getLogger(__name__)
