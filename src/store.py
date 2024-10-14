#%%
import flask

class Store:
  def put_file():
    """Upload a file to the server."""
    file = flask.request.files['file']
    path = flask.request.form['path']
    metadata = flask.request.form['metadata']

    print(f'Writing file to {path}')

    with open("store/"+path, 'wb') as f: f.write(file.read())
    return {"status": "success"}
  
  def list_files():
    """List the files in the store."""
    import os
    return {"files": os.listdir("store")}
  
  def get_file():
    """Download a file from the server."""

  