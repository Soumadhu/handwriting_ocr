import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
import cv2
import numpy as np

# Optional dependency to support PDF uploads without external tools
try:
    import fitz  # PyMuPDF
except Exception:  # pragma: no cover - optional dependency
    fitz = None


def configure_tesseract_on_windows_if_present() -> None:
    """If running on Windows, try to locate tesseract.exe in common paths
    or via TESSERACT_CMD and configure pytesseract accordingly.
    """
    if os.name != 'nt':
        return

    # Respect explicit env var first
    env_cmd = os.environ.get("TESSERACT_CMD")
    if env_cmd and os.path.exists(env_cmd):
        pytesseract.pytesseract.tesseract_cmd = env_cmd
        # Configure tessdata if not already configured
        if not os.environ.get("TESSDATA_PREFIX"):
            base_dir = os.path.dirname(env_cmd)
            tessdata_dir = os.path.join(base_dir, "tessdata")
            if os.path.isdir(tessdata_dir):
                os.environ["TESSDATA_PREFIX"] = base_dir
        return

    common_paths = [
        r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
        r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe",
        r"D:\\tesseract\\tesseract.exe",
    ]
    for candidate in common_paths:
        if os.path.exists(candidate):
            pytesseract.pytesseract.tesseract_cmd = candidate
            if not os.environ.get("TESSDATA_PREFIX"):
                base_dir = os.path.dirname(candidate)
                tessdata_dir = os.path.join(base_dir, "tessdata")
                if os.path.isdir(tessdata_dir):
                    os.environ["TESSDATA_PREFIX"] = base_dir
            return


# Try to auto-configure at startup (safe no-op if not found)
configure_tesseract_on_windows_if_present()

# If on Windows, set path to tesseract.exe
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    extracted_text = None
    error_message = None

    if request.method == "POST":
        if 'file' not in request.files:
            return redirect(request.url)

        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            return redirect(request.url)

        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(filepath)

            filename_lower = filename.lower()
            image = None

            try:
                if filename_lower.endswith('.pdf'):
                    if fitz is None:
                        error_message = (
                            "PDF support requires the 'pymupdf' package. Install it with: pip install pymupdf"
                        )
                    else:
                        with fitz.open(filepath) as pdf_doc:
                            if pdf_doc.page_count == 0:
                                error_message = "The uploaded PDF has no pages."
                            else:
                                page = pdf_doc.load_page(0)
                                pix = page.get_pixmap(dpi=300, alpha=False)
                                img_np = np.frombuffer(pix.samples, dtype=np.uint8)
                                img_np = img_np.reshape(pix.height, pix.width, pix.n)
                                # pix is RGB because alpha=False
                                image = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
                else:
                    # Assume regular image file
                    image = cv2.imread(filepath)

                if image is None:
                    error_message = (
                        "Failed to read the uploaded file. Please upload a valid image (PNG/JPG) or a PDF."
                    )
                else:
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    gray = cv2.threshold(
                        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
                    )[1]

                    # Save processed image for reference
                    processed_path = os.path.join(app.config['UPLOAD_FOLDER'], "processed.png")
                    cv2.imwrite(processed_path, gray)

                    # OCR extraction
                    extracted_text = pytesseract.image_to_string(Image.open(processed_path))
            except Exception as exc:
                error_message = f"Processing failed: {exc}"

    return render_template("index.html", extracted_text=extracted_text, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
