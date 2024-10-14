#%%

from llmservice.llm_api import LLM_API
from llmservice.pdf_api import PDF_API
from llmservice.store import Store

from llmservice.server import server

server(
  LLM_API,
  PDF_API,
  Store,
  port = 5100,
)
