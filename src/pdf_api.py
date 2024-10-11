import flask
import fitz

class PDF_API:
  '''Functions to interact with PDFs.'''

  def handle_pdf():
    '''Extract text from a PDF file. Must be provided as a form-data file upload.'''
    with fitz.open("pdf", flask.request.files['pdf'].read()) as pdf:
      return {'text': ''.join([page.get_text() for page in pdf])}
    
