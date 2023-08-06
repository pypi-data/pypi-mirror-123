"""
Modulo de configuracao da lib de io
"""

import os
from urllib.parse import urlsplit
import json

CONTAINERS = json.loads(os.environ["CONTAINERS"])

storage_options = {
    # default file:// protocol
    "file": {
        None: {
            None: {
                "protocol": "file"
            }
        }
    },

    # main Azure DataLake/Blob account
    "abfs": {}
    }

for key, value in CONTAINERS.items():

    STORAGE_ACCOUNT_URL = urlsplit(value['BASE_FOLDER']).netloc
    STORAGE_ACCOUNT_NAME = STORAGE_ACCOUNT_URL.split(".")[0]

    if "AZURE_STORAGE_KEY" in list(value.keys()):
        base_storage_credentials = {"account_key": value["AZURE_STORAGE_KEY"]}
    else:
        base_storage_credentials = {
            "client_id": value["AZURE_CLIENT_ID"],
            "client_secret": value["AZURE_CLIENT_SECRET"],
            "tenant_id": value["AZURE_TENANT_ID"],
        }

    storage_options['abfs'][STORAGE_ACCOUNT_URL] = {None: {
                                                           "account_name": STORAGE_ACCOUNT_NAME,
                                                           **base_storage_credentials}
                                                   }