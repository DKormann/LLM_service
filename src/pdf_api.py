import flask
import fitz


class PDF_API:
  '''Functions to interact with PDFs.'''

  def handle_pdf():
    '''Extract text from a PDF file.'''
    pdf_data = flask.request.files['pdf']

    with fitz.open("pdf", pdf_data.read()) as pdf:
      text = ''
      for page in pdf:
        text += page.get_text()
    
    return flask.jsonify({"text": text})
