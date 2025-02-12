import os

def generate_aes_key():
    """Generate a 256-bit AES key and save it to a file."""
    aes_key = os.urandom(32)  # 32 bytes = 256-bit key

    # Save the key to a file
    with open("aes_key.key", "wb") as key_file:
        key_file.write(aes_key)
    
    print("AES Key generated and saved as 'aes_key.key'.")

# Run the function
generate_aes_key()