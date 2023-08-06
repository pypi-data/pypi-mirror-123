from dataclasses import dataclass


@dataclass
class MFAError(Exception):
    # botocore.exceptions.ClientError: An error occurred (AccessDenied) when calling the AssumeRole operation:
    # MultiFactorAuthentication failed with invalid MFA one time pass code.
    pass


class AssumeError(Exception):
    # botocore.exceptions.ClientError: An error occurred (AccessDenied) when calling the GetSessionToken operation: Cannot call GetSessionToken with session credentials
    pass


class ClientError(Exception):
    # botocore.exceptions.ClientError: An error occurred (AuthFailure)
    # when calling the DescribeVpcs operation: AWS was not able to validate the provided access credentials
    pass
