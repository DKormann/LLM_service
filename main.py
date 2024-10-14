#%%

from src.llm_api import LLM_API
from src.pdf_api import PDF_API
from src.store import Store

from src.server import server

server(
  # LLM_API,
  # PDF_API,
  # Store,

  port = 5100,
)


#%%
# import flask

# app = flask.Flask(__name__)


# @app.route('/cloud')
# def index():
#   return flask.send_from_directory('./static', 'index.html')



# if __name__ == '__main__':
#   app.run(host='0.0.0.0', port=5100)
