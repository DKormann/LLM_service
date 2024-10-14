import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
  # serve static folder
  return flask.send_from_directory('./static', 'index.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5200)
