from Crypto.Cipher import DES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


SALT_SIZE = 16
IV_SIZE = 8
KEY_SIZE = 8
ITERATIONS = 100_000
MIN_SECRET_LENGTH = 8


def _derive_key(secret_key: str, salt: bytes) -> bytes:
    """Derive a DES key from the user's secret text key."""
    if not secret_key:
        raise ValueError("DES requires a secret key.")
    if len(secret_key) < MIN_SECRET_LENGTH:
        raise ValueError("DES secret key should be at least 8 characters long.")
    return PBKDF2(secret_key, salt, dkLen=KEY_SIZE, count=ITERATIONS)


def encrypt_text(plain_text: str, secret_key: str) -> str:
    """Encrypt text with DES-CBC and return a hex-safe string."""
    if not plain_text:
        raise ValueError("Please enter text to encrypt.")

    salt = get_random_bytes(SALT_SIZE)
    iv = get_random_bytes(IV_SIZE)
    key = _derive_key(secret_key, salt)
    cipher = DES.new(key, DES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(plain_text.encode("utf-8"), DES.block_size))

    return (salt + iv + encrypted).hex()


def decrypt_text(cipher_text: str, secret_key: str) -> str:
    """Decrypt a hex-encoded DES-CBC message created by encrypt_text."""
    try:
        data = bytes.fromhex(cipher_text.strip())
        if len(data) <= SALT_SIZE + IV_SIZE:
            raise ValueError

        salt = data[:SALT_SIZE]
        iv = data[SALT_SIZE:SALT_SIZE + IV_SIZE]
        encrypted = data[SALT_SIZE + IV_SIZE:]
        key = _derive_key(secret_key, salt)
        cipher = DES.new(key, DES.MODE_CBC, iv)

        return unpad(cipher.decrypt(encrypted), DES.block_size).decode("utf-8")
    except (ValueError, KeyError, UnicodeDecodeError) as exc:
        raise ValueError("DES decryption failed. Check the key and encrypted text.") from exc
