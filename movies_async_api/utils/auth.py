import binascii
import hmac
import json
import time
from base64 import b64decode
from hashlib import sha256
from typing import Optional, Tuple

from core.config import AUTH_SECRET_KEY


def is_user_authorize(authorization: str) -> bool:
    access_token = authorization.split(' ', 1)[1]
    if not (token_data := validate_jwt_token(access_token)):
        return False
    header, payload = token_data
    expire_time = payload.get('exp')
    if not expire_time:
        return False
    return time.time() < expire_time


def validate_jwt_token(jwt_token: str) -> Optional[Tuple[dict, dict]]:
    try:
        hashed_header, hashed_payload, input_signature = jwt_token.split('.')
    except ValueError:
        return None
    try:
        header = json.loads(b64decode(hashed_header).decode().replace("'", "\""))
        payload = json.loads(b64decode(hashed_payload).decode().replace("'", "\""))
    except (binascii.Error, json.decoder.JSONDecodeError):
        return None
    alg = header.get('alg')
    if not alg:
        return None
    elif alg == 'HS256':
        digest_mod = sha256
    else:
        return None
    current_signature = hmac.new(
        AUTH_SECRET_KEY.encode(),
        hashed_header.encode() + hashed_payload.encode(),
        digestmod=digest_mod
    ).hexdigest()
    if current_signature != input_signature:
        return None
    return header, payload
