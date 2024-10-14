#%%
import filetype
from PIL import Image
import fitz as pymupdf
import easyocr
from io import BytesIO
import numpy as np
import flask

def handle_pdf():
    '''Extract text from a PDF, DOCX, or image file uploaded as form-data.'''
    if 'file' not in flask.request.files:
        return {'error': 'no File was uploaded'}, 400
    
    uploaded_file = flask.request.files['file']
    
    try:
        extracted_text = get_text_from_document(uploaded_file)
        return {'text': extracted_text}
    except Exception as e:
        return {'error': str(e)}, 500

def get_text_from_document(file_path):
    raw_text = ""
    images = []
    reader = easyocr.Reader(['de']) 

    with open(file_path, 'rb') as uploaded_file:
        file_type = filetype.guess(uploaded_file)
        if file_type.mime == 'application/pdf':
            zoom = 4
            for page in pymupdf.open(stream=uploaded_file.read(), filetype='pdf'):
                images.append(Image.open(BytesIO(page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom)).tobytes("png"))))

        elif 'image' in file_type.mime: images = [Image.open(BytesIO(uploaded_file.read()))]

    for image in images: raw_text += "\n".join([result[1] for result in reader.readtext(np.array(image))]) + "\n"
    return raw_text


