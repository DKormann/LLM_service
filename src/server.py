import flask
from functions import LLMFunctions

app = flask.Flask(__name__)

api_docs = ''

for field in dir(LLMFunctions):
  if field[0] != '_':
    func = getattr(LLMFunctions, field)
    app.route(f'/llm_api/{field}', methods=['POST'], endpoint=field)(lambda: flask.jsonify(func(**flask.request.json)))
    if func.__doc__: api_docs += f'<h3><|host|>/llm_api/{field}</h2><pre>{func.__doc__}</pre>'


default_message = f'<h2>LLM API</h2><p>Available endpoints:</p>{api_docs}'

@app.route('/')
def hello(): return default_message.replace('<|host|>', flask.request.host)

if __name__ == '__main__': app.run(host='0.0.0.0' , port=5100)