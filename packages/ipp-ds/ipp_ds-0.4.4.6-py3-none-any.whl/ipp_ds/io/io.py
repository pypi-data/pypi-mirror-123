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
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

import logging
import fnmatch

from .io_utils import *

# Set the logging level for all azure-* libraries
logger = logging.getLogger('azure')
logger.setLevel(logging.ERROR)

import warnings
warnings.filterwarnings('ignore')

DOWNLOAD_POOL_SIZE = 10
DEFAULT_MAX_RETRIES = 5

def create_blob_service(uri, conn_type='gen2'):

    credential = DefaultAzureCredential(exclude_shared_token_cache_credential=True)

    account_name = uri.replace('abfs://','').split('.')[0]

    if conn_type == 'gen2':
        dlService = DataLakeServiceClient(account_url=f"https://{account_name}.dfs.core.windows.net",
                                          credential = credential)

    if conn_type == 'blob':
        dlService = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net",
                                      credential = credential)

    return dlService

def to_any(df, uri, _format, mode='pandas', encoding='utf-8', conn_type='gen2', **kwargs):

    service_client = create_blob_service(uri=uri, conn_type=conn_type)
    container_name = uri.split('/')[3]
    blob_name = '/'.join(uri.split('/')[4:])

    folder_name, file_name = '/'.join(blob_name.split('/')[:-1]), blob_name.split('/')[-1]

    if conn_type == 'gen2':
        file_system_client = service_client.get_file_system_client(file_system=container_name)
        directory_client = file_system_client.get_directory_client(folder_name)
        file_client = directory_client.create_file(file_name)

    if conn_type == 'blob':
        blob_client = service_client.get_blob_client(container=container_name, blob=blob_name)

    try:
        if _format not in ['csv', 'ppttc']:
            byte_stream = BytesIO()
        else:
            byte_stream = StringIO()

        if mode == 'pyexcelerate': #in development
            format_map = {'excel': pyx_to_excel}
        if mode == 'pandas':
            format_map = {"parquet": df.to_parquet, "csv": df.to_csv, "excel": df.to_excel}
        if mode == 'pptx':
            format_map = {"pptx": df.save}
        if mode == 'thinkcell':
            format_map = {"ppttc": json.dump}

        func = format_map[_format]

        if _format not in ['csv', 'ppttc']:

            if mode != 'pyexcelerate':
                func(byte_stream, **kwargs)
            else:
                func(byte_stream, df, **kwargs)

            byte_stream.seek(0)

            for i in range(DEFAULT_MAX_RETRIES):
                if i > 0:
                    logger.warn(f'Retrying to upload (loop {i}). Error:{e}')
                try:
                    if conn_type == 'gen2':
                        file_client.upload_data(byte_stream, overwrite=True)

                    if conn_type == 'blob':
                        blob_client.upload_blob(byte_stream, overwrite=True)
                    break
                except Exception as e:
                    if i == DEFAULT_MAX_RETRIES-1:
                        raise f'The max retries limit was reached. Error: {e}'
                    pass

        else:
            if _format == 'ppttc':
                func(obj=df.charts, fp=byte_stream,**kwargs)

            else:
                func(byte_stream, encoding=encoding,**kwargs)

            byte_stream.seek(0)

            for i in range(DEFAULT_MAX_RETRIES):
                if i > 0:
                    logger.warn(f'Retrying to upload (loop {i}). Error: {e}')
                try:
                    if conn_type == 'gen2':
                        file_client.upload_data("".join(byte_stream.readlines()), overwrite=True, encoding=encoding)

                    if conn_type == 'blob':
                        blob_client.upload_blob("".join(byte_stream.readlines()), overwrite=True, encoding=encoding)
                    break

                except Exception as e:
                    if i == DEFAULT_MAX_RETRIES-1:
                        raise f'The max retries limit was reached. Error: {e}'
                    pass

    finally:
        byte_stream.close()

def read_any(uri, _format, mode='pandas', conn_type = 'gen2', **kwargs):

    """ Get a dataframe from Parquet file on blob storage """
    service_client = create_blob_service(uri, conn_type = conn_type)
    container_name = uri.split('/')[3]
    blob_name = '/'.join(uri.split('/')[4:])

    if conn_type == 'gen2':
        file_system_client = service_client.get_file_system_client(file_system=container_name)
        file_client = file_system_client.get_file_client(blob_name)

    if conn_type == 'blob':
        blob_client = service_client.get_blob_client(container=container_name, blob=blob_name)

    try:

        byte_stream = BytesIO()

        if conn_type == 'gen2':
            byte_stream.write(file_client.download_file().readall())
        if conn_type == 'blob':
            byte_stream.write(blob_client.download_blob().readall())

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


def to_parquet(df: pd.DataFrame, uri, conn_type = 'gen2', **kwargs):
    return to_any(df, uri, "parquet", conn_type=conn_type, **kwargs)

def to_excel(df: pd.DataFrame, uri, conn_type = 'gen2', mode='pandas', **kwargs):

    #Csv writing currently not supported in blob conn_type
    if mode == 'pyexcelerate':
        logger.warn(f'to_excel method is currently not supported with pyexcelerate mode')
        mode = 'pandas'

    return to_any(df, uri, "excel", conn_type=conn_type, mode=mode, **kwargs)

def to_ppttc(df, uri, conn_type = 'gen2', **kwargs):

    #Csv writing currently not supported in blob conn_type
    if conn_type == 'blob':
        logger.warn(f'to_pptc method is currently not supported with blob conn_type')
        conn_type = 'gen2'

    return to_any(df, uri, "ppttc", mode='thinkcell', conn_type=conn_type, **kwargs)

def to_csv(df: pd.DataFrame, uri, conn_type = 'gen2', encoding='utf-8', **kwargs):

    #Csv writing currently not supported in blob conn_type
    if conn_type == 'blob':
        logger.warn(f'to_csv method is currently not supported with blob conn_type')
        conn_type = 'gen2'

    return to_any(df, uri, "csv", encoding=encoding, conn_type=conn_type, **kwargs)

def to_pptx(df, uri, conn_type = 'gen2', **kwargs):
    return to_any(df, uri, "pptx", mode='pptx', conn_type=conn_type, **kwargs)

def glob(uri, **kwargs):

    blob_service = create_blob_service(uri, conn_type='gen2')
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

def read_parquet(uri, mode='pandas', conn_type = 'gen2', **kwargs):
    return read_any(uri, "parquet", mode=mode, conn_type=conn_type, **kwargs)


def read_csv(uri, mode='pandas', conn_type = 'gen2', **kwargs):
    return read_any(uri, "csv", mode=mode, conn_type=conn_type, **kwargs)


def read_excel(uri, mode='pandas', conn_type = 'gen2', **kwargs):

    # A partir de uma determinada versao, o xlrd parou de dar suporte a xlsx.
    # Usa-se por padrão a engine openpyxl. Se ela não for passada, agnt força a engine
    if ('.xlsx' in uri) & ('engine' not in kwargs):
        kwargs['engine'] = 'openpyxl'

    return read_any(uri, "excel", mode=mode, conn_type=conn_type, **kwargs)

def read_pptx(uri, mode='pptx', conn_type = 'gen2', **kwargs):
    return read_any(uri, "pptx", mode=mode, conn_type=conn_type, **kwargs)

def read_tc_template(uri, _format='pptx', mode='thinkcell', conn_type = 'gen2', **kwargs):
    return read_any(uri, "pptx", mode=mode, conn_type=conn_type, **kwargs)

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
