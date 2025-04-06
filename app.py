from flask import Flask, render_template, request, send_file
import os
from pdf2docx import Converter
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["CONVERTED_FOLDER"] = CONVERTED_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file uploaded", 400
    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # Convert PDF to DOCX
    docx_filename = filename.replace(".pdf", ".docx")
    docx_filepath = os.path.join(app.config["CONVERTED_FOLDER"], docx_filename)

    cv = Converter(filepath)
    cv.convert(docx_filepath, start=0, end=None)
    cv.close()

    return send_file(docx_filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
