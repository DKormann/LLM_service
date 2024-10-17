
#%%
import unittest
from llmservice.pdf_api import PDF_API
from werkzeug.datastructures import FileStorage

doc = 'test/doc.pdf'
doc2 = 'test/flight_acc.pdf'

class TestPDFExtraction(unittest.TestCase):
  def test_extraction_from_doc(self):
    with open("test/doc.pdf", "rb") as f:
      file = FileStorage(f, content_type="application/pdf")
      read_data = PDF_API.get_text_from_document(file)
    assert "Verdienstabrechnung" in read_data
    assert "65200700K024" in read_data

if __name__ == "__main__": unittest.main()