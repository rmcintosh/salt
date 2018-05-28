# Import Python Libs
from __future__ import absolute_import, print_function, unicode_literals
import logging
import pprint
import re
import time
import datetime

# Import Salt Libs
import salt.config as config
from salt.ext import six
from salt.ext.six.moves import range
from salt.exceptions import (
    SaltCloudConfigError,
    SaltCloudException,
    SaltCloudNotFound,
    SaltCloudSystemExit
)


log = logging.getLogger(__name__)
__virtualname__ = 'linode_v4'
API_ROOT = 'https://api.linode.com/v4/'


def __virtual__():
    '''
    Check for Linode API v4 config
    '''
    if get_configured_provider() is False:
        return False

    return __virtualname__

def get_configured_provider():
    '''
    Return the first configured instance.
    '''
    return config.is_provider_configured(
        __opts__,
        __active_provider_name__ or __virtualname__,
        ('token', 'password',)
    )


def _query(endpoint=None, method='GET', params=None, data=None, page=0):
    vm_ = get_configured_provider()

    token = config.get_cloud_config_value('token', vm_, __opts__, search_global=False)

    headers = {
        "Authorization": "Bearer {}".format(token),
        "Accept": "application/json"
    
    }

    url = API_ROOT + endpoint

    result = __utils__['http.query'](url, method=method, params=params, data=data, header_dict=headers, port=443, text=False, decode=True, decode_type='json',  opts=__opts__)

    return result['dict']['data']

def avail_sizes():
    return _query('linode/types')

def avail_locations():
    return _query('regions')
