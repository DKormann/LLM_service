#%%
import requests

def host_llm():
  import llama_cpp
  model_name = 'llama-3-8B-Q8.gguf'
  return llama_cpp.Llama(model_path=f"/shared/weights/{model_name}", verbose=False, n_gpu_layers=-1)

class ClientLLM():
  def __call__(self, **kwargs):
    return requests.post('http://metroplex:5100/llm_completion', json=kwargs).json()
  def create_chat_completion(self, **kwargs):
    return requests.post('http://metroplex:5100/llm_chat_completion', json=kwargs).json()

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
    return Functions.answer(question,response_format={
      "type": "json_object",
      "schema": schema
    })
  
  def extract_invoice_information(text, required_fields=["Titel", "Datum", "Dokument Typ"], optional_fields=["Betrag", "Rechnungsnummer"]):
    '''Extrahiert gefragte Daten felder von gescanntem document, garantiert json output
    params: {
      "text": str,
      "required_fields": List[str] = ["Titel", "Datum", "Dokument Typ"],
      "optional_fields": List[str] = ["Betrag", "Rechnungsnummer"]
    }
    '''

    prompt = f'''Extrahiere folgende Daten von dem gescannten Dokument: {", ".join(required_fields)}
Wenn möglich extrahiere auch: {", ".join(optional_fields)}

Dokument Text:{text}

Antworte in json format.'''
    return Functions.answer_json_schema(prompt, {
      "type": "object",
      "properties": {field: {"type": "string"} for field in required_fields + optional_fields},
      "required": required_fields,
    })


#%%

if __name__ == "__main__":

  print(Functions.answer("What is the capital of France?"))


  print(Functions.answer_json_schema("gib mir beispiel rechnungs daten in json format", 
    {
      "type": "object",
      "properties": {
        "rechnungs_nummer": {"type": "string"},
        "datum": {"type": "string"},
      },
      "required": ["rechnungs_nummer", "datum"],
    }
  ))

  #%%

  print(Functions.extract_invoice_information("Rechnung\nRechnungsnummer: 1234\nDatum: 12.12.2021\nBetrag: 1000€", required_fields=["Rechnungsnummer", "Datum"]))

#%%

  for fun in dir(Functions):
    fn = getattr(Functions, fun)
    if fun[0] != "_" and fn.__doc__:
      print(f"{fun}")
      print(f"{fn.__doc__}")
