# Secure-Image-Steganography
## Project Overview
This project implements Image Steganography using the Least Significant Bit (LSB) technique combined with AES encryption for added security. It allows users to hide text messages inside images securely and extract them when needed.

## Features

### LSB Steganography: Hides secret messages within image pixels.

### AES Encryption: Encrypts messages before embedding for security.

### Flask Web Interface: User-friendly web interface for embedding and extracting messages.

### Supports PNG Images: Works with lossless PNG images to prevent data loss.

#  Installation & Setup
1. Clone the repository:
```
git clone https://github.com/your-username/LSB-Steganography-Encryption.git
cd LSB-Steganography-Encryption
```
2. Create a virtual environment:
```
python3 -m venv myenv
source myenv/bin/activate  # For macOS/Linux
myenv\Scripts\activate     # For Windows
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4 .Generate an AES encryption key:
```
python generate_key.py
```
5. Run the Flask application:
```
python app.py
```
6. Access the web interface at http://127.0.0.1:5000

