import flask
import flask_cors

def server(*handlers, port=5100):
  app = flask.Flask(__name__)

  flask_cors.CORS(app, origins='*')

  docs_css = '''<style>
  body { background-color: #111; font-family: Arial, sans-serif; color: #fff; margin: 5em;}
  h1, h2, h3 {{color: #08f;}}
  @media (prefers-color-scheme: light) {body { background-color: #fff; color: #000; }}
  a{color: unset}
  </style>'''

  def doc_endpoint(docstring, path): app.route(f'/{path}', methods=['GET'], endpoint=path)(lambda: docstring.replace("{host}", flask.request.host) + docs_css)
  def func_endpoint(func, path):
    def handler():
      try: return flask.jsonify(func(**flask.request.json))
      except: return flask.jsonify(func())
    app.route(f'/{path}', methods=['POST'], endpoint=path)(handler)

  root_docs = '<h2>Local ML Services</h2><a href=/cloud>test frontend</a><p>Available APIs:</p>'
  for api in handlers:
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
    
  app.route("/cloud", methods=['GET'])(lambda: flask.send_from_directory('./static', 'index.html'))
  app.route("/cloud/view/<path:path>", methods=['GET'], endpoint='view')(lambda path: flask.send_from_directory('./static', 'view.html'))

  app.errorhandler(400)(lambda e: ("<h1>400</h1><p>Bad request.</p>"+docs_css, 400))
  app.errorhandler(404)(lambda e: ("<h1>404</h1><p>The resource could not be found.</p>"+docs_css, 404))

  app.run(host='0.0.0.0' , port=port)