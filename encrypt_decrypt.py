from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64

# Generate a fixed-size AES key (32 bytes = 256 bits)
password = b"your_secret_password"  # Change this to a strong password
salt = b"1234567890123456"  # Ensure a fixed 16-byte salt (DO NOT CHANGE FOR CONSISTENCY)

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,  # AES-256 key (change to 16 or 24 for AES-128 or AES-192)
    salt=salt,
    iterations=100000,
)

aes_key = kdf.derive(password)  # Ensures a proper 32-byte key


def encrypt_message(message):
    """Encrypts a message using AES CBC mode."""
    message = message.encode("utf-8")  # Convert to bytes
    iv = os.urandom(16)  # Generate a 16-byte IV
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    # Ensure message length is a multiple of 16 (AES block size)
    padding_length = 16 - (len(message) % 16)
    message += bytes([padding_length]) * padding_length  # PKCS7 padding

    encrypted_message = encryptor.update(message) + encryptor.finalize()
    return base64.b64encode(iv + encrypted_message).decode("utf-8")  # Encode IV + encrypted data


def decrypt_message(encrypted_message):
    """Decrypts a message using AES CBC mode."""
    encrypted_message = base64.b64decode(encrypted_message)  # Decode Base64
    iv = encrypted_message[:16]  # Extract IV
    encrypted_data = encrypted_message[16:]  # Extract encrypted content

    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    decrypted_message = decryptor.update(encrypted_data) + decryptor.finalize()

    # Remove PKCS7 padding
    padding_length = decrypted_message[-1]
    return decrypted_message[:-padding_length].decode("utf-8")