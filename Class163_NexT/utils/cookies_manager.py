import os
import json
from cryptography.fernet import Fernet
from netease_encode_api import EncodeSession

KEY_FILE = os.path.expanduser("~/.class163_next_key")
COOKIE_FILE = os.path.expanduser("~/.class163_next_cookies")

def _get_key():
    fernet_key: bytes = b""
    if not os.path.exists(KEY_FILE):
        fernet_key = Fernet.generate_key()
        os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
        with open(KEY_FILE, "wb") as f:
            f.write(fernet_key)
        os.chmod(KEY_FILE, 0o600)
    else:
        with open(KEY_FILE, "rb") as f:
            fernet_key = f.read()
    return fernet_key

def load_cookies() -> EncodeSession:
    if not os.path.exists(COOKIE_FILE): return EncodeSession()
    fernet_key = Fernet(_get_key())
    session = EncodeSession()
    with open(COOKIE_FILE, "rb") as f:
         session.cookies.update(json.loads(fernet_key.decrypt(f.read())))
    return session

def save_cookies(session: EncodeSession) -> bool:
    fernet_key = Fernet(_get_key())
    data = json.dumps(session.cookies.get_dict()).encode()
    with open(COOKIE_FILE, "wb") as f:
        f.write(fernet_key.encrypt(data))
    return True

def cookies_exists() -> bool: return os.path.exists(COOKIE_FILE)