def host_llm():
  import llama_cpp
  model_name = 'llama-3-8B-Q8.gguf'
  return llama_cpp.Llama(model_path=f"/shared/weights/{model_name}", verbose=False, n_gpu_layers=-1)

import requests
class ClientLLM():
  def __call__(self, **kwargs):
    return requests.post('http://metroplex:5100/llm_completion', json=kwargs).json()
  
  def create_chat_completion(self, **kwargs):
    return requests.post('http://metroplex:5100/llm_chat_completion', json=kwargs).json()
