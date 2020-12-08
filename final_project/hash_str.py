import hashlib
from typing import Union
from dotenv import load_dotenv
import os

load_dotenv()


def get_csci_salt() -> bytes:
    """Returns the appropriate salt for CSCI E-29

    :return: bytes representation of the CSCI salt
    """
    # Hint: use os.environment and bytes.fromhex
    salt_hex = os.environ.get('CSCI_SALT')
    salt_bytes = bytes.fromhex(salt_hex)
    return salt_bytes


def hash_str(some_val: Union[str, bytes], salt: Union[str, bytes] = "") -> bytes:
    """Converts strings to hash digest

    See: https://en.wikipedia.org/wiki/Salt_(cryptography)

    :param some_val: thing to hash, can be str or bytes
    :param salt: Add randomness to the hashing, can be str or bytes
    :return: sha256 hash digest of some_val with salt, type bytes
    """
    if type(salt) is None:
        salt = get_csci_salt()
    if type(salt) == str:
        salt = salt.encode()
    if type(some_val) not in (str, bytes):
        some_val = str(some_val)
    if type(some_val) == str:
        some_val = some_val.encode()
    var_sha = hashlib.sha256()
    var_sha.update(salt)
    var_sha.update(some_val)
    str_digest = var_sha.digest()
    return str_digest


def get_user_id(username: str) -> str:
    salt = get_csci_salt()
    return hash_str(username.lower(), salt=salt).hex()[:8]
