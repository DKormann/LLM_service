#%%
import requests
from llm import host_llm, ClientLLM

if requests.get("http://metroplex:5100/").status_code == 200:
  print("LLM server is up")
  llm = ClientLLM()
else:
  print("LLM server is down")
  llm = host_llm()

def answer(question):
  return llm.create_chat_completion(
    
  )
