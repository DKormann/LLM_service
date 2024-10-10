import flask

app = flask.Flask(__name__)

from functions import Functions

api_docs = ''

for field in dir(Functions):
  if field[0] != '_':
    func = getattr(Functions, field)
    @app.route(f'/llm_api/{field}')
    def wrapper(): return func(**flask.request.json)
    if func.__doc__: api_docs += f'<h3>{{host}}/llm_api/{field}</h2><p>{func.__doc__}</p>'

default_message = f'<h2>LLM API</h2><p>Available endpoints:</p>{api_docs}'
@app.route('/')
def hello(): return default_message.format(host=flask.request.host)

if __name__ == '__main__': app.run(host='0.0.0.0' , port=5100)