from typing import Optional
from smart_crypt import decrypt, encrypt

try:
    from django.conf import settings

    SECRET_KEY = settings.SECRET_KEY
except ImportError:
    SECRET_KEY = None


def encode(string: str, secret: Optional[str] = SECRET_KEY):
    if not secret:
        raise ValueError('miss secret')
    return encrypt(string, secret)


def decode(enc: str, secret: Optional[str] = SECRET_KEY):
    if not secret:
        raise ValueError('miss secret')
    return decrypt(enc, secret)
