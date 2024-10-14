#%%
import filetype
from PIL import Image
import fitz as pymupdf
import easyocr
from io import BytesIO
from docx import Document
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
            uploaded_file.seek(0) # needed if you want to reread the file
            pdf = pymupdf.open(stream=uploaded_file.read(), filetype='pdf')
            for page in pdf:
                zoom = 8
                mat = pymupdf.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                img = Image.open(BytesIO(img_data))
                images.append(img)

        elif file_type.extension == 'docx':
            uploaded_file.seek(0)
            doc = Document(uploaded_file)
            for para in doc.paragraphs:
                raw_text += para.text + " "

        elif 'image' in file_type.mime:
            uploaded_file.seek(0)
            images = [Image.open(BytesIO(uploaded_file.read()))]

    for image in images:
        np_image = np.array(image)
        results = reader.readtext(np_image)
        raw_text += "\n".join([result[1] for result in results]) + "\n"

    return raw_text

file_path = 'r-20131231-andresen.pdf'  # change to the path of the file you want to extract text from
extracted_text = get_text_from_document(file_path)
print(extracted_text)
# %%
