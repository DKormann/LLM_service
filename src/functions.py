#%%
import requests
from llm import host_llm, ClientLLM

try:
  requests.get("http://metroplex:5100/")
  print("LLM server is up connecting to it.")
  llm = ClientLLM()
except:
  print("Launching local LLM.")
  llm = host_llm()

#%%
class Functions:
  '''Functions to interact with the LLM model.'''
  
  def chat_completion(**kwargs): return llm.create_chat_completion(**kwargs)['choices'][0]['message']['content']

  def answer(question, **kwargs):
    '''just answer the question text -> text
    params: {"question": str}
    '''
    return Functions.chat_completion(
      messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": question}],
      **kwargs)

  def answer_json(question):
    '''answer the question with guaranteed json output text -> json
    params: {"question": str}
    '''
    return Functions.answer(question, response_format={"type":"json_object"})

  def answer_json_schema(question):
    pass
#%%

if __name__ == "__main__":
  # print(Functions.answer("What is the capital of the United States?"))
  # print(Functions.answer_json("What is the capital of the United States? [answer in json format]"))


  for fun in dir(Functions):
    fn = getattr(Functions, fun)
    if fun[0] != "_" and fn.__doc__:
      print(f"{fun}")
      print(f"{fn.__doc__}")
