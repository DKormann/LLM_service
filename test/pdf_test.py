import unittest
from llmservice.pdf_api import get_text_from_document

doc = 'test/doc.pdf'
doc2 = 'test/flight_acc.pdf'

class TestPDFExtraction(unittest.TestCase):
  def test_extraction_from_doc(self):
    extracted_text = get_text_from_document(doc2)
    assert "Booking No. 35160458884" in extracted_text

if __name__ == "__main__": unittest.main()