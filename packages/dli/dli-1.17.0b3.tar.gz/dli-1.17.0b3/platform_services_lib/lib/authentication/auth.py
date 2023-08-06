import os
import requests
from urllib.parse import urljoin
from typing import Optional
from ..context.environments import _Environment
from ..context.urls import sam_urls, identity_urls


def sam_app_flow(environment: _Environment) -> Optional[str]:
    # Retrieve SAM-token using DLI_ACCESS_KEY_ID and DLI_SECRET_ACCESS_KEY
    # Retrieve client JWT from catalogue using SAM-token and DLI_ACCESS_KEY_ID
    DLI_ACCESS_KEY_ID = os.environ.get('DLI_ACCESS_KEY_ID')
    DLI_SECRET_ACCESS_KEY = os.environ.get('DLI_SECRET_ACCESS_KEY')
    if DLI_SECRET_ACCESS_KEY is None or DLI_ACCESS_KEY_ID is None:
        return None

    sam_env = environment.sam
    catalogue_env = environment.catalogue
    catalogue_url = urljoin(catalogue_env, identity_urls.identity_token)
    sam_url = urljoin(sam_env, sam_urls.sam_token)

    sam_payload = {
        'client_id': DLI_ACCESS_KEY_ID,
        'client_secret': DLI_SECRET_ACCESS_KEY,
        'grant_type': 'client_credentials'
    }
    resp = requests.post(sam_url, data=sam_payload)
    if resp.status_code != 200:
        raise Exception('Could not retrieve jwt access token with client credentials')

    sam_token = resp.json()['access_token']
    dl_payload = {
        'client_id': DLI_ACCESS_KEY_ID,
        'subject_token': sam_token
    }
    resp = requests.post(catalogue_url, data=dl_payload)
    jwt = resp.json()['access_token']
    return jwt
