#%%
import requests


model_name = 'llama-3-8B-Q8.gguf'

def host_llm():
  import llama_cpp
  return llama_cpp.Llama(model_path=f"/shared/weights/{model_name}", verbose=False, n_gpu_layers=-1, n_ctx=0)

class ClientLLM():
  def __call__(self, **kwargs): return requests.post('http://metroplex:5100/llm_api/llm_call', json=kwargs).json()
  def create_chat_completion(self, **kwargs): return requests.post('http://metroplex:5100/llm_api/chat_completion', json=kwargs).json()

try:
  requests.get("http://metroplex:5100/")
  print("LLM server is up connecting to it.")
  llm = ClientLLM()
except:
  print("Launching local LLM.")
  llm = host_llm()

#%%
class LLM_API:
  f'''Functions to interact with the LLM model'''
  
  def llm_call(**kwargs): return llm(**kwargs)
  def chat_completion(**kwargs): return llm.create_chat_completion(**kwargs)

  def answer(question, **kwargs):
    '''just answer the question text -> text
    params: {"question": str}
    '''
    return LLM_API.chat_completion(
      messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": question}],
      **kwargs)['choices'][0]['message']['content']

  def answer_json(question):
    '''answer the question with guaranteed json output text -> json
    params: {"question": str}
    '''
    return LLM_API.answer(question, response_format={"type":"json_object"})


  def answer_json_schema(question, schema):
    '''answer the question with guaranteed json output conforming to a provided schema text -> json
    params: {"question": str, "schmema": dict}

    Example schema:
    {
      "type": "object",
      "properties": {
        "rechnungs_nummer": {"type": "string"},
        "datum": {"type": "string"},
      },
      "required": ["rechnungs_nummer", "datum"],
    },
    '''
    return LLM_API.answer(question,response_format={
      "type": "json_object",
      "schema": schema
    })
  
  def extract_invoice_information(text, required_fields=["Titel", "Datum", "Dokument Typ"], optional_fields=["Betrag", "Rechnungsnummer"], additional_prompt=""):
    '''Extrahiert gefragte Daten felder von gescanntem document, garantiert json output
    Zusätzliche Anweisungen können unter additional_prompt auf deutsch spezifiziert werden.
    params: {
      "text": str,
      "required_fields": List[str] = ["Titel", "Datum", "Dokument Typ"],
      "optional_fields": List[str] = ["Betrag", "Rechnungsnummer"],
      "additional_prompt": str = ''
    }
    '''

    if len(text) > 8000: text = text[:4000] + '[...]' + text[-4000:]

    prompt = f'''Extrahiere folgende Daten von dem gescannten Dokument: {", ".join(required_fields)}
Wenn möglich extrahiere auch: {", ".join(optional_fields)}

Dokument Text:{text}

Antworte in json format.
{additional_prompt}'''

    return LLM_API.answer_json_schema(prompt, {
      "type": "object",
      "properties": {field: {"type": "string"} for field in required_fields + optional_fields},
      "required": required_fields,
    })

#%%

if __name__ == "__main__":

  print(LLM_API.answer("What is the capital of France?"))
  #%%
  print(LLM_API.answer_json_schema("gib mir beispiel rechnungs daten in json format", 
    {
      "type": "object",
      "properties": {
        "rechnungs_nummer": {"type": "string"},
        "datum": {"type": "string"},
      },
      "required": ["rechnungs_nummer", "datum"],
    }
  ))
  print(LLM_API.extract_invoice_information("Rechnung\nRechnungsnummer: 1234\nDatum: 12.12.2021\nBetrag: 1000€", required_fields=["Rechnungsnummer", "Datum"]))

#%%

  for fun in dir(LLM_API):
    fn = getattr(LLM_API, fun)
    if fun[0] != "_" and fn.__doc__:
      print(f"{fun}")
      print(f"{fn.__doc__}")
