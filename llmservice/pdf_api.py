from PIL import Image
import fitz as pymupdf
import easyocr
from io import BytesIO
import numpy as np
import flask

class PDF_API:
  """Handling PDF OCR"""
  @staticmethod
  def handle_pdf():
    '''Extract text from a PDF, DOCX, or image file uploaded as form-data.'''
    if 'file' not in flask.request.files:
      return {'error': 'No file was uploaded'}, 400
    
    uploaded_file = flask.request.files['file']
    extracted_text = PDF_API.get_text_from_document(uploaded_file)
    return {'text': extracted_text}

  @staticmethod
  def get_text_from_document(uploaded_file):
    raw_text = ""
    images = []
    reader = easyocr.Reader(['de'])  
    file_type = uploaded_file.mimetype 
    if file_type == 'application/pdf':
      zoom = 4
      pdf_doc = pymupdf.open(stream=uploaded_file.read(), filetype='pdf')  
      for page in pdf_doc:
        pixmap = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
        images.append(Image.open(BytesIO(pixmap.tobytes("png")))) 
    elif 'image' in file_type:
      images = [Image.open(BytesIO(uploaded_file.read()))]  
    # Perform OCR on the images
    for image in images:
      raw_text += "\n".join([result[1] for result in reader.readtext(np.array(image))]) + "\n"
    return raw_text
