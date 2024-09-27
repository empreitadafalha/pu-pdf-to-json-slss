import os
import json
import fitz  # PyMuPDF
import pandas as pd
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from flask import Flask, request, jsonify

app = Flask(__name__)

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
    return text

def extract_tables_from_pdf(pdf_path):
    # Using a placeholder function as table extraction can be complex
    # This should be replaced with actual table extraction logic, such as using camelot or tabula-py
    return []

def convert_images_to_text(images):
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

def pdf_to_json(pdf_path):
    pdf_data = {}
    pdf_data['text'] = extract_text_from_pdf(pdf_path)
    pdf_data['tables'] = extract_tables_from_pdf(pdf_path)

    images = convert_from_path(pdf_path)
    pdf_data['image_text'] = convert_images_to_text(images)

    return pdf_data

@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.pdf'):
        pdf_path = '/tmp/' + file.filename
        file.save(pdf_path)
        pdf_data = pdf_to_json(pdf_path)
        os.remove(pdf_path)  # Clean up the temporary file
        return jsonify(pdf_data)
    else:
        return jsonify({'error': 'Invalid file type'}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))