#%%
from llmservice.llm_api import LLM_API
from llmservice.pdf_api import PDF_API
from llmservice.store import Store
from llmservice.server import server

import sys

server(
  LLM_API,
  PDF_API,
  Store,
  port = sys.argv[1] if len(sys.argv) > 1 else 5100,
)
