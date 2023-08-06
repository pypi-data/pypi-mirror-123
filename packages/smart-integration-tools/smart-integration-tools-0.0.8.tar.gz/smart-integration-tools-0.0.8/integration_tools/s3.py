import os
import boto3
from boto3.s3.transfer import TransferConfig
from io import StringIO, BytesIO
from typing import Union

from .settings import parse_tools_settings

BUCKET_NAME, DASHBOARD_URL, _, _ = parse_tools_settings()

__all__ = (
    'upload_to_s3',
    'check_s3_file_exist',
    'get_s3_file_link',
    'delete_s3_file',
    'upload_to_s3_from_ram',
)


def upload_to_s3(filename: str, folder: str = "stats/") -> dict:
    """Upload file to s3

    Args:
        filename (str): file name
        folder (str, optional): s3 folder. Defaults to "stats/".

    Returns:
        dict: result
    """
    s3 = boto3.resource('s3')
    GB = 1024 ** 3
    config = TransferConfig(multipart_threshold=int(GB / 3))
    if filename.startswith('/tmp/'):
        s3_filename = filename[5:]
    else:
        s3_filename = filename
    s3.meta.client.upload_file(
        filename,
        BUCKET_NAME,
        f"{folder}{s3_filename}",
        ExtraArgs={'ACL': 'public-read'},
        Config=config,
    )

    return {"status": "success", "s3_filename": s3_filename, "s3_folder": folder}


def check_s3_file_exist(filename: str, folder: str = "stats/") -> bool:
    """Check file in s3 bucket

    Args:
        filename (str): filename
        folder (str, optional): s3 folder. Defaults to "stats/".

    Returns:
        bool: True if exist else False
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    if filename.startswith('/tmp/'):
        filename = filename[5:]
    key = folder + filename
    objs = list(bucket.objects.filter(Prefix=key))
    if len(objs) > 0 and objs[0].key == key:
        return True
    else:
        return False


def get_s3_file_link(
    filename: str,
    folder: str = 'stats/',
    bucket: str = BUCKET_NAME,
    extension: str = '.tsv',
) -> str:
    """Get file link for s3 fileobj

    Args:
        filename (str): filenam
        folder (str, optional): s3 folder. Defaults to 'stats/'.
        bucket (str, optional): s3 bucket. Defaults to BUCKET_NAME.
        extension (str, optional): file extension. Defaults to '.tsv'.

    Returns:
        str: [description]
    """
    client = boto3.client('s3')
    if filename.startswith('/tmp/'):
        filename = filename[5:]
    if extension in filename:
        filename = f"{folder}{filename}" if folder not in filename else filename
    else:
        filename = (
            f"{folder}{filename}{extension}"
            if folder not in filename
            else f"{filename}{extension}"
        )
    # content = client.head_object(Bucket=BUCKET_NAME, Key=filename)
    bucket_location = client.get_bucket_location(Bucket=bucket)
    filepath = f"https://s3-{bucket_location['LocationConstraint']}.amazonaws.com/{bucket}/{filename}"

    return filepath


def delete_s3_file(
    filename: str, folder: str, extension: str, bucket: str = BUCKET_NAME
) -> str:
    """Delete file from s3

    Args:
        filename (str): filename
        folder (str): s3 folder
        extension (str): file extension
        bucket (str, optional): s3 bucket name. Defaults to BUCKET_NAME.

    Returns:
        str: result
    """
    if filename.startswith('/tmp/'):
        filename = filename[5:]
    client = boto3.client('s3')
    if extension not in filename:
        filename = f"{filename}{extension}"
    if folder not in filename:
        filename = f"{folder}{filename}"
    client.delete_object(Bucket=bucket, Key=filename)
    return f"{filename} - deleted!"


def upload_to_s3_from_ram(
    content: Union[StringIO, BytesIO],
    filename: str,
    folder: str = 'stats/',
    extension: str = '.tsv',
    bucket: str = BUCKET_NAME,
) -> dict:
    """upload s3 file from RAM

    Args:
        content (Union[StringIO, BytesIO]): file date
        filename (str): filename
        folder (str, optional): s3 folder. Defaults to 'yandex_files/'.
        extension (str, optional): file extension. Defaults to '.tsv'.
        bucket (str, optional): s3 bucket name. Defaults to BUCKET_NAME.

    Returns:
        dict: result
    """
    if filename.startswith('/tmp/'):
        s3_filename = filename[5:]
    else:
        s3_filename = filename
    if extension not in s3_filename:
        s3_filename = f"{s3_filename}{extension}"
    s3 = boto3.resource('s3')
    body = (
        content.getvalue().encode('utf-8')
        if isinstance(content, StringIO)
        else content.getvalue()
    )
    s3.meta.client.put_object(
        Bucket=bucket, Key=f'{folder}{s3_filename}', Body=body, ACL='public-read'
    )
    return {"status": "success", "s3_filename": s3_filename, "s3_folder": folder}
