import tempfile
from io import BytesIO, StringIO
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Tuple
from urllib.request import urlretrieve
from urllib.parse import urlsplit
from pptx import Presentation
from thinkcell import Thinkcell
import json

import pandas as pd

from ipp_io import storage_options

import adal
from azure.storage.blob import (BlobServiceClient)
from azure.identity import ClientSecretCredential

DOWNLOAD_POOL_SIZE = 10

def create_blob_service(uri):

    cred=get_storage_options(uri)

    RESOURCE = '/'.join(uri.split('/')[:3]).replace('abfs','https').replace('dfs','blob')
    clientId = cred['client_id']
    clientSecret = cred['client_secret']
    tenantId = cred['tenant_id']
    authority_url = "https://login.microsoftonline.com/" + tenantId

    credential = ClientSecretCredential(client_id=clientId,
                                        client_secret=clientSecret,
                                        tenant_id=tenantId)

    blobService = BlobServiceClient(account_url="{}://{}.blob.core.windows.net".format("https",cred['account_name']), credential=credential)

    return blobService

def to_any(df, uri, _format, mode='pandas', encoding='utf-8', **kwargs):

    blob_service = create_blob_service(uri)
    container_name = uri.split('/')[3]
    blob_name = '/'.join(uri.split('/')[4:])

    blob_client = blob_service.get_blob_client(container=container_name, blob=blob_name)

    try:
        if _format not in ['csv', 'ppttc']:
            byte_stream = BytesIO()
        else:
            byte_stream = StringIO()

        if mode == 'pandas':
            format_map = {"parquet": df.to_parquet, "csv": df.to_csv, "excel": df.to_excel}
        if mode == 'pptx':
            format_map = {"pptx": df.save}
        if mode == 'thinkcell':
            format_map = {"ppttc": json.dump}

        func = format_map[_format]

        if _format not in ['csv', 'ppttc']:

            func(byte_stream, **kwargs)
            byte_stream.seek(0)
            blob_client.upload_blob(byte_stream, overwrite=True)

        else:
            if _format == 'ppttc':
                func(obj=df.charts, fp=byte_stream,**kwargs)

            else:
                func(byte_stream, encoding=encoding,**kwargs)

            byte_stream.seek(0)
            blob_client.upload_blob("".join(byte_stream.readlines()), overwrite=True)

    finally:
        byte_stream.close()



def read_any(uri, _format, mode='pandas',**kwargs):

    """ Get a dataframe from Parquet file on blob storage """
    blob_service = create_blob_service(uri)
    container_name = uri.split('/')[3]
    blob_name = '/'.join(uri.split('/')[4:])

    blob_client = blob_service.get_blob_client(container=container_name, blob=blob_name)

    try:

        byte_stream = BytesIO()
        byte_stream.write(blob_client.download_blob(max_concurrency=16).readall())
        byte_stream.seek(0)

        if mode == 'pandas':
            format_map = {"parquet": pd.read_parquet, "csv": pd.read_csv, "xls": pd.read_excel}
        if mode == 'pptx':
            format_map = {'pptx': Presentation}

        if mode == 'thinkcell':
            df = Thinkcell()
            df.add_template(uri)

        if mode != 'thinkcell':
            func = format_map[_format]
            df = func(byte_stream, **kwargs)

    finally:
        byte_stream.close()

    return df


def to_parquet(df: pd.DataFrame, uri, **kwargs):
    return to_any(df, uri, "parquet", **kwargs)


def to_excel(df: pd.DataFrame, uri, **kwargs):
    return to_any(df, uri, "excel", **kwargs)

def to_ppttc(df, uri, **kwargs):
    return to_any(df, uri, "ppttc", mode='thinkcell', **kwargs)

def to_csv(df: pd.DataFrame, uri, encoding='utf-8', **kwargs):
    return to_any(df, uri, "csv", encoding=encoding,**kwargs)

def to_pptx(df, uri, **kwargs):
    return to_any(df, uri, "pptx", mode='pptx', **kwargs)

def walk(uri, **kwargs):

    blob_service = create_blob_service(uri)
    container_name = uri.split('/')[3]
    blob_name = '/'.join(uri.split('/')[4:])
    url_name = '/'.join(uri.split('/')[:4])
    container_client = blob_service.get_container_client(container=container_name)
    list_blobs = [url_name+'/'+unit['name'] for unit in container_client.list_blobs(name_starts_with=f'{blob_name}/')]

    return list_blobs

def glob(uri, **kwargs):

    blob_service = create_blob_service(uri)
    container_name = uri.split('/')[3]
    blob_name = '/'.join(uri.split('/')[4:])
    url_name = '/'.join(uri.split('/')[:3])
    container_client = blob_service.get_container_client(container=container_name)
    list_blobs = [url_name+'/'+container_name+'/'+unit['name'] for unit in container_client.walk_blobs(name_starts_with=f'{blob_name}/')]

    return list_blobs

def read_parquet(uri, mode='pandas', **kwargs):
    return read_any(uri, "parquet", mode=mode, **kwargs)


def read_csv(uri, mode='pandas', **kwargs):
    return read_any(uri, "csv", mode=mode, **kwargs)


def read_excel(uri, mode='pandas', **kwargs):
    return read_any(uri, "xls", mode=mode, **kwargs)

def read_pptx(uri, mode='pptx', **kwargs):
    return read_any(uri, "pptx", mode=mode, **kwargs)

def read_tc_template(uri, _format='pptx', mode='thinkcell', **kwargs):
    return read_any(uri, "pptx", mode=mode, **kwargs)


def get_storage_options(uri) -> Dict[str, Any]:
    # decompose uri
    u = urlsplit(uri)

    scheme = u.scheme or "file"
    host = f"{u.hostname}:{u.port}" if u.port else u.hostname
    host = host if host else None
    user = u.username if u.username else None

    # get possible matching keys
    keys = [(scheme, host, user), (scheme, host, None), (scheme, None, None)]

    opts: Dict[str, Any] = None
    for _scheme, _host, _user in keys:
        try:
            opts = storage_options[_scheme][_host][_user]
            break
        except KeyError:
            pass

    # try to match a wildcard
    if opts is None:
        raise Exception(
            f"Key not found in storage_options: ({scheme}, {host}, {user})"
        )

    # Augment options with known URI components
    opts.setdefault("protocol", scheme)
    return opts


def read_url(uri, sas_token, _format, **kwargs):
    """Read from a container with SAS token """
    with tempfile.NamedTemporaryFile() as tf:
        url_tok = uri + sas_token
        urlretrieve(url_tok, tf.name)
        df = read_any(uri=tf.name, _format=_format, **kwargs)
        return df
