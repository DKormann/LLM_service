#%%
import llama_cpp

model_name = 'llama-3-8B-Q8.gguf'
llm = llama_cpp.Llama(
  model_path=f"/shared/weights/{model_name}",
  n_gpu_layers=-1,)

llama_prompt_template = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n{system_message}<|eot_id|><|start_header_id|>user<|end_header_id|>\n{question}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
default_system_message = "You are a helpful assistant"

def answer(question:str, system_message=default_system_message, prompt_template=llama_prompt_template, max_tokens=100, **kwargs):
  prompt = prompt_template.format(system_message=system_message, question=question)
  resp = llm(prompt, stop = ["<|start_header_id|>"], max_tokens=max_tokens, **kwargs)
  return resp['choices'][0]['text']

#%%
def answer_json(question:str, system_message=default_system_message, prompt_template=llama_prompt_template, max_tokens=100, **kwargs):
  response = llm.create_chat_completion(
    messages=[
      {"role": "system", "content": system_message},
      {"role": "user", "content": question},
    ],
    response_format={'type': 'json_object'},
    max_tokens=max_tokens,
    **kwargs
  )
  return response['choices'][0]['message']['content']


#%%
if __name__ == '__main__':
  print(answer_json("give me json data about russia containing population, gdp, and area"))

  #%%

  print(answer("give me data about russia containing population, gdp, and area"))
  
