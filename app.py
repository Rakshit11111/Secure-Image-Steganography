from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
from embed_extract import embed_message, extract_message
from encrypt_decrypt import encrypt_message, decrypt_message
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # For flash messages

# Define upload folders
UPLOAD_FOLDER = "static/uploads/"
STEGO_FOLDER = "static/stego_images/"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STEGO_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file is an allowed image format."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/embed', methods=['POST'])
def embed():
    if "image" not in request.files or "message" not in request.form:
        flash("Please upload an image and enter a message.")
        return redirect(url_for("index"))
    
    image = request.files["image"]
    message = request.form["message"].strip()
    
    if image.filename == "" or not allowed_file(image.filename):
        flash("Invalid file type! Only PNG, JPG, and JPEG are allowed.")
        return redirect(url_for("index"))
    
    if not message:
        flash("Message cannot be empty.")
        return redirect(url_for("index"))
    
    filename = secure_filename(image.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    stego_path = os.path.join(STEGO_FOLDER, "stego_" + filename)
    
    image.save(image_path)

    # Encrypt message properly
    encrypted_msg = encrypt_message(message)  # Now returns bytes
    embed_message(image_path, encrypted_msg, stego_path)  # Embed in image
    
    return send_file(stego_path, as_attachment=True)

@app.route('/extract', methods=['POST'])
def extract():
    if "stego_image" not in request.files:
        flash("Please upload a stego image.", "error")
        return redirect(url_for("index"))
    
    image = request.files["stego_image"]
    
    if image.filename == "" or not allowed_file(image.filename):
        flash("Invalid file type! Only PNG, JPG, and JPEG are allowed.", "error")
        return redirect(url_for("index"))
    
    filename = secure_filename(image.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    
    image.save(image_path)
    
    # Extract the encrypted message
    extracted_result = extract_message(image_path)
    
    if not extracted_result:
        flash("Error: No hidden message found in the image.", "error")
        return redirect(url_for("index"))
    
    extracted_encrypted_msg = extracted_result[-1]  # Extract only the message
    
    if not extracted_encrypted_msg or len(extracted_encrypted_msg) < 16:
        flash("Error: Extracted data is too short or corrupted.", "error")
        return redirect(url_for("index"))
    
    print(f"Extracted Message (Base64): {extracted_encrypted_msg}")
    
    try:
        decrypted_msg = decrypt_message(extracted_encrypted_msg)
        print(f"Decrypted Message: {decrypted_msg}")
    except Exception as e:
        flash(f"Decryption failed: {str(e)}", "error")
        return redirect(url_for("index"))
    
    return render_template("index.html", extracted_message=decrypted_msg)

if __name__ == "__main__":
    app.run(debug=True)