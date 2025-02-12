from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64

# Generate a fixed-size AES key (32 bytes = 256 bits)
password = b"your_secret_password"  # Change this to a strong password
salt = b"1234567890123456"  # 16-byte fixed salt for consistency

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,  # AES-256 key
    salt=salt,
    iterations=100000,
)

aes_key = kdf.derive(password)  # Generates a 32-byte AES key

def pad_message(message):
    """Applies PKCS7 padding to make message length a multiple of 16 bytes."""
    padding_length = 16 - (len(message) % 16)
    return message + bytes([padding_length]) * padding_length

def unpad_message(padded_message):
    """Removes PKCS7 padding from the decrypted message."""
    padding_length = padded_message[-1]
    if padding_length < 1 or padding_length > 16:
        raise ValueError("Invalid padding detected!")
    return padded_message[:-padding_length]

def encrypt_message(message):
    """Encrypts a message using AES CBC mode."""
    message = message.encode("utf-8")  # Convert to bytes
    iv = os.urandom(16)  # Generate a 16-byte IV
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    padded_message = pad_message(message)  # Apply PKCS7 padding
    encrypted_message = encryptor.update(padded_message) + encryptor.finalize()

    return base64.b64encode(iv + encrypted_message).decode("utf-8")  # Encode IV + encrypted data


def decrypt_message(encrypted_message):
    """Decrypts a message using AES CBC mode."""
    try:
        encrypted_message = base64.b64decode(encrypted_message)  # Decode Base64
        
        if len(encrypted_message) < 16:
            raise ValueError(f"Invalid encrypted message length: {len(encrypted_message)}. Expected at least 16 bytes.")
            
        iv = encrypted_message[:16]  # Extract IV
        encrypted_data = encrypted_message[16:]  # Extract encrypted content
        
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        
        decrypted_padded_message = decryptor.update(encrypted_data) + decryptor.finalize()
        
        # Remove PKCS7 padding
        padding_length = decrypted_padded_message[-1]
        return decrypted_padded_message[:-padding_length].decode("utf-8")
    
    except Exception as e:
        return f"Decryption failed: {str(e)}"  # Return error message for debugging