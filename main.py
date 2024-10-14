#%%

from src.llm_api import LLM_API
from src.pdf_api import PDF_API
from src.store import Store

from src.server import server

server(
  LLM_API,
  PDF_API,
  Store,

  port = 5100,
)
