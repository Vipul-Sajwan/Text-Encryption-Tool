from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


IV_SIZE = 16
VALID_KEY_SIZES = (16, 24, 32)


def _validate_key(secret_key: str) -> bytes:
    """Validate and return an AES key of 16, 24, or 32 bytes."""
    if not secret_key:
        raise ValueError("AES requires a secret key.")

    key = secret_key.encode("utf-8")
    if len(key) not in VALID_KEY_SIZES:
        raise ValueError(
            "AES key must be exactly 16, 24, or 32 bytes long "
            "for AES-128, AES-192, or AES-256."
        )
    return key


def encrypt_text(plain_text: str, secret_key: str) -> str:
    """Encrypt text with AES-CBC and return a hex-safe string."""
    if not plain_text:
        raise ValueError("Please enter text to encrypt.")

    iv = get_random_bytes(IV_SIZE)
    key = _validate_key(secret_key)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(plain_text.encode("utf-8"), AES.block_size))

    return (iv + encrypted).hex()


def decrypt_text(cipher_text: str, secret_key: str) -> str:
    """Decrypt a hex-encoded AES-CBC message created by encrypt_text."""
    try:
        data = bytes.fromhex(cipher_text.strip())
        if len(data) <= IV_SIZE:
            raise ValueError

        iv = data[:IV_SIZE]
        encrypted = data[IV_SIZE:]
        key = _validate_key(secret_key)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        return unpad(cipher.decrypt(encrypted), AES.block_size).decode("utf-8")
    except (ValueError, KeyError, UnicodeDecodeError) as exc:
        raise ValueError("AES decryption failed. Check the key and encrypted text.") from exc
