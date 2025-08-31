import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
from werkzeug.utils import secure_filename
import mimetypes

# Load environment variables
load_dotenv()

# Verify API key exists
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

# Configure Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Flask app
app = Flask(__name__)

# Directory to temporarily store uploaded files
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".pdf", ".doc", ".docx"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    if not user_msg:
        return jsonify({"response": "No message provided."}), 400

    try:
        # Generate response
        chat = model.start_chat()
        response = chat.send_message(user_msg)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"Error processing message: {str(e)}"}), 500

@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if "file" not in request.files:
            return jsonify({"response": "No file provided."}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"response": "No file selected."}), 400

        if not allowed_file(file.filename):
            return jsonify({"response": "Invalid file type. Please upload an image, PDF, or Word document."}), 400

        # Securely save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Determine MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = "application/octet-stream"

        # Prepare file for Gemini API
        try:
            uploaded_file = genai.upload_file(path=file_path, mime_type=mime_type)
            chat = model.start_chat()
            response = chat.send_message([uploaded_file, "Analyze this file and provide a summary or relevant response."])

            # Clean up the file after processing
            if os.path.exists(file_path):
                os.remove(file_path)

            return jsonify({"response": response.text})
        except Exception as e:
            # Clean up the file in case of error
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({"response": f"Error processing file: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"response": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)