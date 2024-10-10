import flask

app = flask.Flask(__name__)

default_message = 'this is the llm server.\nyou can ask a question at <a href="http://{host}/answer/your question">http://{host}/answer/your question</a>'
@app.route('/')
def hello(): return default_message.format(host=flask.request.host)

from src.llm import host_llm
llm = host_llm()

@app.route('llm_completion', methods=['POST'])
def llm_completion():
  params = flask.request.json
  return llm(**params)

@app.route("llm_chat_completion", methods=['POST'])
def llm_chat_completion():
  params = flask.request.json
  return llm.create_chat_completion(**params)

if __name__ == '__main__': app.run(host='0.0.0.0' , port=5100)