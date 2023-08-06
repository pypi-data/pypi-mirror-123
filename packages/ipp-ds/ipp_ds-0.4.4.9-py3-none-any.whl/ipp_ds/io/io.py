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
DEFAULT_CHUNK_SIZE = 100*1024*1024

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

def to_any(byte_stream, uri, encoding='utf-8', conn_type='gen2'):

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

    byte_stream.seek(0)

    for i in range(DEFAULT_MAX_RETRIES):
        try:
            if conn_type == 'gen2':
                if isinstance(byte_stream, BytesIO):
                    file_client.upload_data(byte_stream, overwrite=True, chunk_size=DEFAULT_CHUNK_SIZE)
                else:
                    file_client.upload_data("".join(byte_stream.readlines()), overwrite=True, encoding=encoding, chunk_size=DEFAULT_CHUNK_SIZE)

            if conn_type == 'blob':
                if isinstance(byte_stream, BytesIO):
                    blob_client.upload_blob(byte_stream, overwrite=True)
                else:
                    blob_client.upload_blob("".join(byte_stream.readlines()), overwrite=True, encoding=encoding)
            break
        except Exception as e:
            logger.warn(f'Retrying to upload (loop {i+1}). Error:{e}')
            if i == DEFAULT_MAX_RETRIES-1:
                raise Exception(f'The max retries limit was reached. Error: {e}')
            pass

def read_any(uri, func, conn_type = 'gen2', **kwargs):

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

        df = func(byte_stream, **kwargs)

    finally:
        byte_stream.close()

    return df


def to_parquet(df: pd.DataFrame, uri, conn_type = 'gen2', **kwargs):
    byte_stream = BytesIO()
    df.to_parquet(byte_stream, **kwargs)
    return to_any(byte_stream, uri, conn_type=conn_type)

def to_excel(df: pd.DataFrame, uri, conn_type = 'gen2', mode='pandas', **kwargs):

    #Csv writing currently not supported in blob conn_type
    if mode == 'pyexcelerate':
        logger.warn(f'to_excel method is currently not supported with pyexcelerate mode')
        mode = 'pandas'

    byte_stream = BytesIO()
    func_dict = {'pandas': pd.DataFrame.to_excel, 'pyexcelerate': pyx_to_excel}
    func_dict[mode](df, byte_stream, **kwargs)

    return to_any(byte_stream, uri, conn_type=conn_type)

def to_ppttc(df, uri, conn_type = 'gen2', **kwargs):

    #Csv writing currently not supported in blob conn_type
    if conn_type == 'blob':
        logger.warn(f'to_pptc method is currently not supported with blob conn_type')
        conn_type = 'gen2'
    
    byte_stream = StringIO()
    func = json.dump
    func(obj=df.charts, fp=byte_stream, **kwargs)

    return to_any(byte_stream, uri, conn_type=conn_type)

def to_csv(df: pd.DataFrame, uri, conn_type = 'gen2', encoding='utf-8', **kwargs):

    #Csv writing currently not supported in blob conn_type
    if conn_type == 'blob':
        logger.warn(f'to_csv method is currently not supported with blob conn_type')
        conn_type = 'gen2'

    byte_stream = StringIO()
    df.to_csv(byte_stream, encoding=encoding, **kwargs)
    return to_any(byte_stream, uri, encoding=encoding, conn_type=conn_type)

def to_pptx(df, uri, conn_type = 'gen2', **kwargs):
    byte_stream = BytesIO()
    df.save(byte_stream, **kwargs)
    return to_any(byte_stream, uri, conn_type=conn_type)

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
    func = {'pandas': pd.read_parquet}
    func = func[mode]
    return read_any(uri, func, conn_type=conn_type, **kwargs)


def read_csv(uri, mode='pandas', conn_type = 'gen2', **kwargs):
    func = {'pandas': pd.read_csv}
    func = func[mode]
    return read_any(uri, func, conn_type=conn_type, **kwargs)


def read_excel(uri, mode='pandas', conn_type = 'gen2', **kwargs):

    # A partir de uma determinada versao, o xlrd parou de dar suporte a xlsx.
    # Usa-se por padrão a engine openpyxl. Se ela não for passada, agnt força a engine
    if ('.xlsx' in uri) & ('engine' not in kwargs):
        kwargs['engine'] = 'openpyxl'

    func = {'pandas': pd.read_excel}
    func = func[mode]
    return read_any(uri, func, conn_type=conn_type, **kwargs)

def read_pptx(uri, mode='pptx', conn_type = 'gen2', **kwargs):
    func = {'pptx': Presentation}
    func = func[mode]
    return read_any(uri, func, conn_type=conn_type, **kwargs)

def read_tc_template(uri, _format='pptx', mode='thinkcell', conn_type = 'gen2', **kwargs):
    df = Thinkcell()
    df.add_template(uri)
    return df

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
