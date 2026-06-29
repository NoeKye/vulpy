import hashlib
import secrets
import os
from pathlib import Path
import libuser
import logging
logger = logging.getLogger("vulpy.api")

API_KEY_DIR = Path('./.apikeys')
API_KEY_DIR.mkdir(exist_ok=True)


def keygen(username, password=None):

    if password:
        if not libuser.login(username, password):
            return None

    key = hashlib.sha256(secrets.token_bytes(256)).hexdigest()

    for f in API_KEY_DIR.glob('vulpy.apikey.' + username + '.*'):
        print('removing', f)
        try:
            f.unlink()
        except Exception as e:
            print(f"Không thể xóa file {f}: {e}")
            continue

    keyfile = API_KEY_DIR / 'vulpy.apikey.{}.{}'.format(username, key)

    Path(keyfile).touch()

    return key


def authenticate(request):
    if 'X-APIKEY' not in request.headers:
        return None

    key = request.headers['X-APIKEY']

    for f in API_KEY_DIR.glob('vulpy.apikey.*.' + key):
        current_user = f.name.split('.')[2]
        logger.info(f"Yêu cầu API hợp lệ từ người dùng: '{current_user}'")
        return current_user
    logger.error(f"Phát hiện truy cập API trái phép với Key không hợp lệ: {key[:8]}...")
    return None
