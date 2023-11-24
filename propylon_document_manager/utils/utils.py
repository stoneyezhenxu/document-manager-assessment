import os
import re
import logging
import uuid
import hashlib
from pathlib import Path
from typing import Optional
from django.conf import settings

from .global_value import GlobalValue


# get file uuuid
def get_uuid() -> str:
    return memoryview(uuid.uuid1().bytes)[:32].hex()


# format file size -> xxB, xxKB, xxMB, xxGB
def format_file_size(file_size: float, round_num=2) -> str:
    if file_size < 1024:
        size = f'{file_size}B'
    elif file_size < 1048576:
        size = f'{round(file_size / 1024, round_num)}KB'
    elif file_size < 1073741824:
        size = f'{round(file_size / 1024 / 1024, round_num)}M'
    else:
        size = f'{round(file_size / 1024 / 1024 / 1024, round_num)}G'
    return size


# format file type -> 'docs', 'imgs', 'videos' ,'procedure', 'others'
def format_file_type(file_type: str) -> str:
    file_type = file_type.lower()
    if file_type in GlobalValue.ImgsSet:
        new_file_type = GlobalValue.ImgsType
    elif file_type in GlobalValue.DocsSet:
        new_file_type = GlobalValue.DocsType
    elif file_type in GlobalValue.VideoSet:
        new_file_type = GlobalValue.VideosType
    elif file_type in GlobalValue.ProcedureSet:
        new_file_type = GlobalValue.ProcedureType
    else:
        new_file_type = GlobalValue.OthersType
    return new_file_type


def valid_request_for_files_post(request_data: dict) -> tuple[dict, str]:
    error_infos = ''
    new_request_data = {
        GlobalValue.FileObj: request_data.get(GlobalValue.FileObj, None),
        GlobalValue.FileName: request_data.get(GlobalValue.FileName, ''),
        GlobalValue.FileUrl: request_data.get(GlobalValue.FileUrl, ''),
        GlobalValue.FileDesc: request_data.get(GlobalValue.FileDesc, ''),
        GlobalValue.FileType: format_file_type(file_type=request_data.get(GlobalValue.FileName, '').split('.')[-1]),
        GlobalValue.FileSize: format_file_size(file_size=float(request_data.get(GlobalValue.FileSize, 0))),
        GlobalValue.FileUuid: get_uuid(),
        GlobalValue.FileNameHash: get_file_name_hashcode(request_data.get(GlobalValue.FileUrl, ''))
    }

    # file size limit
    if float(request_data.get(GlobalValue.FileSize, 0)) > GlobalValue.PostFileLimitSize:
        error_infos = GlobalValue.PostFileLimitSizeError
    # file name require
    if new_request_data[GlobalValue.FileName] == '':
        error_infos = GlobalValue.PostFileNameError
    # file url require
    if new_request_data[GlobalValue.FileUrl] == '':
        error_infos = GlobalValue.PostFileUrlError

    return new_request_data, error_infos


def get_local_file_path(file_uuid: str, file_name: str, file_type: str) -> str:
    dir_path = Path("{}/{}/{}/".format(settings.APPS_DIR, 'static', file_type))
    file_path = os.path.join(dir_path, '{}_{}'.format(file_uuid, file_name))

    return file_path


def save_file_to_local(file_uuid: str, file_name: str, file_type: str, file_obj: Optional):
    dir_path = Path("{}/{}/{}/".format(settings.APPS_DIR, 'static', file_type))
    os.makedirs(dir_path,exist_ok=True)

    file_path = os.path.join(dir_path, '{}_{}'.format(file_uuid, file_name))

    try:
        with open(file_path, 'wb') as file:
            for chunk in file_obj.chunks():
                file.write(chunk)
        logging.info("File success saved! file_path:{}".format(file_path))
    except Exception as e:
        logging.info("File fail saved! error is:{} ".format(e))


# get hashcode by file_name
def get_file_name_hashcode(file_name: str) -> str:
    m = hashlib.md5()
    m.update(file_name.encode())
    m.digest()
    return m.hexdigest()


def validate_email(email: str) -> bool:
    rex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(rex, email):
        return True
    return False


def validate_password_or_username(data: str) -> bool:
    n = len(data)
    if n < 3 or n > 15:
        return False
    return True


def validate_register_fields(username: str, email: str, password: str) -> str:
    if not validate_password_or_username(username):
        return GlobalValue.UsernameError
    if not validate_email(email):
        return GlobalValue.EmailFormatError
    if not validate_password_or_username(password):
        return GlobalValue.PasswordError
    return ''
