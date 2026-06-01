import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


def generate_key_pair() -> tuple[str, str]:
    """Generate a 2048-bit RSA public/private key pair in PEM format."""
    key = RSA.generate(2048)
    private_key = key.export_key().decode("utf-8")
    public_key = key.publickey().export_key().decode("utf-8")
    return public_key, private_key


def encrypt_text(plain_text: str, public_key_pem: str) -> str:
    """Encrypt text with an RSA public key and return Base64 ciphertext."""
    if not plain_text:
        raise ValueError("Please enter text to encrypt.")
    if not public_key_pem.strip():
        raise ValueError("RSA encryption requires a public key.")

    try:
        public_key = RSA.import_key(public_key_pem)
        cipher = PKCS1_OAEP.new(public_key)
        encrypted = cipher.encrypt(plain_text.encode("utf-8"))
        return base64.b64encode(encrypted).decode("utf-8")
    except (ValueError, TypeError) as exc:
        raise ValueError("RSA encryption failed. Check the public key and text length.") from exc


def decrypt_text(cipher_text: str, private_key_pem: str) -> str:
    """Decrypt Base64 RSA ciphertext with a private key."""
    if not private_key_pem.strip():
        raise ValueError("RSA decryption requires a private key.")

    try:
        private_key = RSA.import_key(private_key_pem)
        cipher = PKCS1_OAEP.new(private_key)
        encrypted = base64.b64decode(cipher_text.strip())
        decrypted = cipher.decrypt(encrypted)
        return decrypted.decode("utf-8")
    except (ValueError, TypeError, UnicodeDecodeError) as exc:
        raise ValueError("RSA decryption failed. Check the private key and encrypted text.") from exc
