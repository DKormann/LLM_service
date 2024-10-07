import flask
from llm import answer

default_message = 'this is the llm server.\nyou can ask a question at <a href="http://{host}/answer/your question">http://{host}/answer/your question</a>'

app = flask.Flask(__name__)

@app.route('/')
def hello(): return default_message.format(host=flask.request.host)

@app.route('/answer/<string:question>')
def get_answer(question):
  if question == '': default_message.format(host=flask.request.host)
  return answer(question)

@app.route('/answer', methods=['POST'])
def post_answer():
  params = flask.request.json
  question = params['question']
  sys_message = params.get('system_message', "You are a helpful assistant")
  return answer(question, system_message=sys_message)

if __name__ == '__main__': app.run(host='0.0.0.0' , port=5100)