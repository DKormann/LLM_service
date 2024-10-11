import flask

from llm_api import LLM_API
from pdf_api import PDF_API

apis = [
  LLM_API,
  PDF_API]

app = flask.Flask(__name__)

docs_css = '''<style>
body { background-color: #123; font-family: Arial, sans-serif; color: #fff; margin: 5em;}
h1, h2, h3 {{color: #08f;}}
@media (prefers-color-scheme: light) {body { background-color: #fff; color: #000; }}
</style>'''


def doc_endpoint(docstring, path): app.route(f'/{path}', methods=['GET'], endpoint=path)(lambda: docstring.replace("{host}", flask.request.host) + docs_css)
def func_endpoint(func, path): app.route(f'/{path}', methods=['POST'], endpoint=path)(lambda: flask.jsonify(func(**flask.request.json)))

root_docs = '<h2>Local ML Services</h2><p>Available APIs:</p>'
for api in apis:
  path = api.__name__.lower()
  root_docs += f'<h3><a href="/{path}">{{host}}/{path}</a></h3>' + (f'<pre>{api.__doc__}</pre>' if api.__doc__ else '')
  api_docs = f'<h2><a href="/">{{host}}</a>/{path}</h2><pre>{api.__doc__}</pre>'

  for field in dir(api):
    if field[0] != '_':
      func = getattr(api, field)
      if func.__doc__: api_docs += f'<h3>{{host}}/{path}/{field}</h2><pre>{func.__doc__}</pre>'
      func_endpoint(func, f'{path}/{field}')
  doc_endpoint(api_docs, path)

doc_endpoint(root_docs, '')

if __name__ == '__main__': app.run(host='0.0.0.0' , port=5100)