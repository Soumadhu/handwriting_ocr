# handwriting_ocr
a basic image to text scanner


# Handwriting OCR Web Application

A Flask-based web application that converts handwritten text from images and PDFs into digital text using Optical Character Recognition (OCR).

## Features

- **Image Support**: Upload and process PNG, JPG, JPEG images
- **PDF Support**: Upload and process PDF documents (first page)
- **Web Interface**: Simple and intuitive web-based UI
- **Text Extraction**: Extract handwritten text using Tesseract OCR
- **Cross-platform**: Works on Windows, macOS, and Linux

## Prerequisites

Before running this application, you need to install Tesseract OCR:

### Windows
1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install it to a directory (e.g., `C:\Program Files\Tesseract-OCR\`)
3. Add the installation directory to your system PATH

### macOS
```bash
brew install tesseract
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install tesseract-ocr
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd handwriting_ocr
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv myenv
   ```

3. **Activate the virtual environment:**
   - Windows: `myenv\Scripts\activate`
   - macOS/Linux: `source myenv/bin/activate`

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Open your web browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **Upload an image or PDF file** containing handwritten text

4. **Click "Scan"** to process the document

5. **View the extracted text** displayed on the page

## Project Structure

```
handwriting_ocr/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
├── .gitignore         # Git ignore file
├── static/
│   └── style.css      # CSS styling
├── templates/
│   └── index.html     # HTML template
└── uploads/           # Upload directory (created automatically)
```

## How It Works

1. **File Upload**: Users upload images or PDFs through the web interface
2. **Image Processing**: 
   - PDFs are converted to images (first page only)
   - Images are converted to grayscale and binarized for better OCR
3. **OCR Processing**: Tesseract OCR extracts text from the processed image
4. **Result Display**: Extracted text is displayed to the user

## Dependencies

- **Flask**: Web framework
- **pytesseract**: Python wrapper for Tesseract OCR
- **Pillow**: Image processing
- **OpenCV**: Computer vision library for image preprocessing
- **PyMuPDF**: PDF processing (optional)
- **NumPy**: Numerical computing
- **Werkzeug**: WSGI utilities

## Troubleshooting

### Tesseract Not Found
If you get a "Tesseract not found" error:
1. Ensure Tesseract is installed and in your system PATH
2. On Windows, the app will automatically search common installation paths
3. You can set the `TESSERACT_CMD` environment variable to point to your tesseract.exe

### PDF Support Issues
If PDF processing fails:
1. Install PyMuPDF: `pip install pymupdf`
2. Ensure the PDF is not corrupted or password-protected

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues and enhancement requests! 
