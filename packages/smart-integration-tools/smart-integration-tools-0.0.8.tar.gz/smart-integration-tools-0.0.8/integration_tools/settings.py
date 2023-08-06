import os
from typing import Optional

__all__ = ('init_tools_settings', 'parse_tools_settings')


def init_tools_settings(
    s3_bucket_name: str,
    dashboard_url: str,
    execute_token: str,
    credential_model_path: Optional[str] = None,
):
    """init tool settings

    Args:
        s3_bucket_name (str): default s3 bucket
        dashboard_url (str): url for dashboard app
        credential_model_path (Optional[str]): model path for credential
    """
    os.environ['TOOLS_BUCKET_NAME'] = s3_bucket_name
    os.environ['TOOLS_EXECUTE_TOKEN'] = execute_token
    os.environ['TOOLS_DASHBOARD_URL'] = (
        dashboard_url if dashboard_url.endswith("/") else f'{dashboard_url}/'
    )
    if credential_model_path:
        os.environ['TOOLS_CREDENTIAL_MODEL_PATH'] = credential_model_path


def parse_tools_settings() -> tuple:
    BUCKET_NAME = os.environ.get('TOOLS_BUCKET_NAME')
    DASHBOARD_URL = os.environ.get('TOOLS_DASHBOARD_URL')
    CREDENTIAL_MODEL = os.environ.get('TOOLS_CREDENTIAL_MODEL_PATH')
    execute_token = os.environ.get('TOOLS_EXECUTE_TOKEN')
    if not BUCKET_NAME or not DASHBOARD_URL:
        raise ValueError('BUCKET_NAME or DASHBOARD_URL not enabled')
    return BUCKET_NAME, DASHBOARD_URL, CREDENTIAL_MODEL, execute_token
