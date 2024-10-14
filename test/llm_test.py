import unittest
from llmservice.llm_api import LLM_API

import json

class TestLLM(unittest.TestCase):
  def test_answer(self):
    answer = LLM_API.answer("What is the capital of France?")
    assert "paris" in answer.lower()
  
  def test_answer_json(self):
    answer = LLM_API.answer_json("What is the capital of France? (answer in json please)")
    assert "paris" in answer.lower()
    data = json.loads(answer)
  
if __name__ == "__main__": unittest.main()