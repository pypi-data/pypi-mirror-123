import tempfile
from io import BytesIO, StringIO
from urllib.request import urlretrieve
from pptx import Presentation
from thinkcell import Thinkcell
import json

import pandas as pd
import numpy as np
import re

from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import DefaultAzureCredential

import logging
import fnmatch

# Set the logging level for all azure-* libraries
logger = logging.getLogger('azure')
logger.setLevel(logging.ERROR)

import warnings
warnings.filterwarnings('ignore')

DOWNLOAD_POOL_SIZE = 10

def create_blob_service(uri):

    credential = DefaultAzureCredential(exclude_shared_token_cache_credential=True)

    account_name = uri.replace('abfs://','').split('.')[0]

    dlService = DataLakeServiceClient(account_url=f"https://{account_name}.dfs.core.windows.net",
                                      credential = credential)

    return dlService

def to_any(df, uri, _format, mode='pandas', encoding='utf-8', **kwargs):

    service_client = create_blob_service(uri)
    container_name = uri.split('/')[3]
    blob_name = '/'.join(uri.split('/')[4:])

    folder_name, file_name = '/'.join(blob_name.split('/')[:-1]), blob_name.split('/')[-1]

    file_system_client = service_client.get_file_system_client(file_system=container_name)
    directory_client = file_system_client.get_directory_client(folder_name)
    file_client = directory_client.create_file(file_name)

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
            file_client.upload_data(byte_stream, overwrite=True, timeout=1800) #0.5h de timeout

        else:
            if _format == 'ppttc':
                func(obj=df.charts, fp=byte_stream,**kwargs)

            else:
                func(byte_stream, encoding=encoding,**kwargs)

            byte_stream.seek(0)
            file_client.upload_data("".join(byte_stream.readlines()), overwrite=True)

    finally:
        byte_stream.close()

def read_any(uri, _format, mode='pandas',**kwargs):

    """ Get a dataframe from Parquet file on blob storage """
    service_client = create_blob_service(uri)
    container_name = uri.split('/')[3]
    blob_name = '/'.join(uri.split('/')[4:])

    file_system_client = service_client.get_file_system_client(file_system=container_name)
    file_client = file_system_client.get_file_client(blob_name)

    try:

        byte_stream = BytesIO()
        byte_stream.write(file_client.download_file().readall())
        byte_stream.seek(0)

        if mode == 'pandas':
            format_map = {"parquet": pd.read_parquet, "csv": pd.read_csv, "excel": pd.read_excel}
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

def glob(uri, **kwargs):

    blob_service = create_blob_service(uri)
    container_name = uri.split('/')[3]
    container_url = '/'.join(uri.split('/')[:4])
    blob_name = '/'.join(uri.split('/')[4:])
    container_client = blob_service.get_file_system_client(file_system=container_name)

    if '*' in blob_name:
        path = blob_name.split("*")[0]
        path_suffix = '*'.join(blob_name.split("*")[1:])
    else:
        path = blob_name.rstrip('/')
        path_suffix = ''

    try:
        list_blobs = [container_url+'/'+unit.name for unit in container_client.get_paths(path=path, **kwargs)]
    except:
        new_path = '/'.join(path.split('/')[:-1])
        path_suffix = path.split('/')[-1]+'*'+path_suffix
        list_blobs = [container_url+'/'+unit.name for unit in container_client.get_paths(path=new_path, **kwargs)]

    result_list = []

    if len(list_blobs) == 0:
        print('Does not have any file that match the specified criteria')
        return result_list

    if len(path_suffix) == 0:
        return list_blobs

    else:
        path_suffix = fnmatch.translate(path_suffix)
        for i in np.array(list_blobs):                
            match = re.search(path_suffix, i)
            if match is not None:
                result_list.append(i)

    return result_list

def read_parquet(uri, mode='pandas', **kwargs):
    return read_any(uri, "parquet", mode=mode, **kwargs)


def read_csv(uri, mode='pandas', **kwargs):
    return read_any(uri, "csv", mode=mode, **kwargs)


def read_excel(uri, mode='pandas', **kwargs):

    # A partir de uma determinada versao, o xlrd parou de dar suporte a xlsx.
    # Usa-se por padrão a engine openpyxl. Se ela não for passada, agnt força a engine
    if ('.xlsx' in uri) & ('engine' not in kwargs):
        kwargs['engine'] = 'openpyxl'

    return read_any(uri, "excel", mode=mode, **kwargs)

def read_pptx(uri, mode='pptx', **kwargs):
    return read_any(uri, "pptx", mode=mode, **kwargs)

def read_tc_template(uri, _format='pptx', mode='thinkcell', **kwargs):
    return read_any(uri, "pptx", mode=mode, **kwargs)

def read_url(uri, sas_token, _format, **kwargs):
    """Read from a container with SAS token """
    with tempfile.NamedTemporaryFile() as tf:
        url_tok = uri + sas_token
        urlretrieve(url_tok, tf.name)
        df = read_any(uri=tf.name, _format=_format, **kwargs)
        return df


def file_exists(path):
    """ Checa se o arquivo informado existe """
    last_dir = path.replace(path.split('/')[-1], "*")

    if path in glob(last_dir):
        return True
    else:
        return False
