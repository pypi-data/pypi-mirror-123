"""
Python package created to automate auditing tasks for resources that live in the cloud.
"""

import logging
from offprem.offprem import (VirtualPrivateCloud, Profile, ConfigureCredentials, ConfigureVPC, AWSPremise,
                             SecurityTokenService)

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(logging.NullHandler())
