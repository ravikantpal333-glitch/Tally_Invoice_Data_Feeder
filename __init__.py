
from flask import Flask, render_template, request, jsonify
from pathlib import Path
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024

MAX_FILES = 10


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_invoice():
    files = request.files.getlist("invoice")
    sales_people = request.form.getlist("sales_person")
    invoice_types = request.form.getlist("invoice_type")

    if not files or all(not file.filename for file in files):
        return jsonify({
            "success": False,
            "message": "Please select at least one PDF."
        }), 400

    if len(files) > MAX_FILES:
        return jsonify({
            "success": False,
            "message": "Maximum 10 PDFs are allowed."
        }), 400

    errors = []
    valid_files = []
    batch_names = set()

    for index, file in enumerate(files):
        original_name = file.filename

        if not original_name:
            errors.append(f"Row {index + 1}: Please select a PDF.")
            continue

        if Path(original_name).suffix.lower() != ".pdf":
            errors.append(f"{original_name}: Only PDF files are allowed.")
            continue

        filename = secure_filename(original_name)

        if not filename:
            errors.append(f"Row {index + 1}: Invalid filename.")
            continue

        name_key = filename.casefold()

        if name_key in batch_names:
            errors.append(f"{original_name}: Duplicate filename in this batch.")
            continue

        batch_names.add(name_key)

        if (UPLOAD_FOLDER / filename).exists():
            errors.append(f"{original_name}: This filename already exists.")

        if index >= len(sales_people) or not sales_people[index].strip():
            errors.append(f"{original_name}: Select a Sales Person.")
            continue

        if index >= len(invoice_types) or not invoice_types[index].strip():
            errors.append(f"{original_name}: Select a Type.")
            continue

        valid_files.append({
            "file": file,
            "filename": filename,
            "sales_person": sales_people[index],
            "invoice_type": invoice_types[index]
        })

    if errors:
        return jsonify({
            "success": False,
            "message": "Please fix the following errors.",
            "errors": errors
        }), 400

    saved_files = []

    try:
        for item in valid_files:
            file_path = UPLOAD_FOLDER / item["filename"]
            item["file"].save(file_path)
            saved_files.append(file_path)

    except Exception:
        for file_path in saved_files:
            file_path.unlink(missing_ok=True)

        app.logger.exception("Batch upload failed.")

        return jsonify({
            "success": False,
            "message": "Upload failed. Please try again."
        }), 500

    return jsonify({
        "success": True,
        "message": f"{len(saved_files)} PDF(s) uploaded successfully.",
        "files": [path.name for path in saved_files]
    })


@app.errorhandler(413)
def file_too_large(error):
    return jsonify({
        "success": False,
        "message": "Total upload size exceeds 20 MB."
    }), 413
