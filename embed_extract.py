import cv2
import numpy as np

def embed_message(image_path, message, stego_path):
    """Embeds an encrypted message in an image using LSB steganography."""
    
    # Convert message string to bytes
    message_bytes = message.encode('utf-8')  # Ensure it's bytes
    
    # Convert bytes to binary representation
    binary_msg = ''.join(format(byte, '08b') for byte in message_bytes) + '1111111111111110'  # End delimiter
    
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Error loading image. Check the file path.")
        
    # Ensure dtype is uint8
    image = image.astype(np.uint8)
    
    # Embed the binary message in the image using LSB
    index = 0
    rows, cols, _ = image.shape
    
    for row in range(rows):
        for col in range(cols):
            for channel in range(3):  # RGB channels
                if index < len(binary_msg):
                    pixel = int(image[row, col, channel])  # Ensure pixel is treated as int
                    pixel = (pixel & ~1) | int(binary_msg[index])  # Modify LSB
                    image[row, col, channel] = np.uint8(pixel)  # Convert back to uint8
                    index += 1
                else:
                    break
            
    # Save the stego image
    cv2.imwrite(stego_path, image)
    print(f"Message embedded successfully in '{stego_path}'")



def extract_message(stego_path):
    """Extracts an embedded message from an image."""
    
    # Load the image
    image = cv2.imread(stego_path)
    if image is None:
        raise ValueError("Error loading stego image. Check the file path.")
        
    binary_msg = ""
    end_marker = '1111111111111110'  # End marker to detect message termination
    
    for row in image:
        for pixel in row:
            for channel in range(3):  # Iterate over RGB channels
                binary_msg += str(pixel[channel] & 1)
            
                if binary_msg.endswith(end_marker):  
                    binary_msg = binary_msg[:-len(end_marker)]  # Remove end marker
                    
                    # Convert binary to bytes
                    byte_data = bytes(int(binary_msg[i:i+8], 2) for i in range(0, len(binary_msg), 8))
                    
                    # Convert bytes to string
                    extracted_text = byte_data.decode('utf-8', errors='ignore')
                    
                    # Debugging Output
                    print("Debug: Extracted Binary (First 200 bits):", binary_msg[:200])
                    print("Debug: Extracted Bytes (First 50):", byte_data[:50])
                    
                    return binary_msg, extracted_text  # Return both binary and extracted message
            
    raise ValueError("No hidden message found in the image.")