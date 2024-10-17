import unittest
from llmservice.pdf_api import PDF_API

doc = 'test/doc.pdf'
doc2 = 'test/flight_acc.pdf'

class TestPDFExtraction(unittest.TestCase):
  def test_extraction_from_doc(self):
    # extracted_text = PDF_API.get_text_from_document(doc2)
    # assert "Booking No. 35160458884" in extracted_text
    pass

if __name__ == "__main__": unittest.main()