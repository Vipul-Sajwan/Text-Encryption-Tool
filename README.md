# Text Encryption Tool

Text Encryption Tool is a beginner-friendly Python cybersecurity project that encrypts and decrypts text using AES, DES, and RSA. It uses a compact Tkinter GUI and keeps the focus on execution, encryption correctness, and modular code.

## Project Structure

```text
TextEncryptionTool/
|-- main.py
|-- gui.py
|-- aes_encrypt.py
|-- des_encrypt.py
|-- rsa_encrypt.py
|-- utils.py
|-- requirements.txt
`-- README.md
```

## Installation

1. Open a terminal in the `TextEncryptionTool` folder.
2. Install the required dependency:

```bash
pip install pycryptodome
```

## Run the Application

```bash
python main.py
```

## Algorithms

### AES

AES, or Advanced Encryption Standard, is a modern symmetric encryption algorithm. The same secret key is used for encryption and decryption. This project uses AES in CBC mode with PKCS7-style padding and a random IV. The AES key must be exactly 16, 24, or 32 bytes long for AES-128, AES-192, or AES-256.

### DES

DES, or Data Encryption Standard, is an older symmetric encryption algorithm. It is included here for learning purposes, but it is no longer recommended for real-world security because its key size is too small. This project uses DES in CBC mode with padding, a random salt, a random IV, and PBKDF2 key derivation.

### RSA

RSA is an asymmetric encryption algorithm. It uses a public key for encryption and a private key for decryption. The application can generate a new 2048-bit RSA key pair and uses OAEP padding for safer RSA encryption.

## Usage

1. Enter text in the input text area.
2. Select `AES`, `DES`, or `RSA` from the algorithm dropdown.
3. For AES, enter a key that is exactly 16, 24, or 32 bytes long. Examples: `1234567890abcdef` for AES-128, `1234567890abcdef12345678` for AES-192, or `1234567890abcdef1234567890abcdef` for AES-256.
4. For DES, enter a secret phrase of at least 8 characters. The app derives the real DES key from this phrase using PBKDF2.
5. For RSA, click `Generate RSA Keys` or paste an existing public/private PEM key into the key field. Use the public key to encrypt and the private key to decrypt.
6. Click `Encrypt` to encrypt the input text.
7. Copy the encrypted output, paste it into the input area, enter the matching key, and click `Decrypt` to recover the original text.
8. Use `Copy Output` to copy results to the clipboard.
9. Use `Clear` to reset the text areas and key field.

## Important Notes

- AES and DES encrypted output is shown as hex text.
- RSA encrypted output is shown as Base64 text.
- RSA can only encrypt small amounts of text directly. For larger data, a hybrid approach should be used.
- DES is included for educational comparison only and should not be used for production security.

## Future Improvements

- Add file encryption and decryption.
- Add hybrid RSA plus AES encryption for larger messages.
- Add password visibility toggle.
- Add key import and export buttons.
- Add automated unit tests for all crypto modules.
