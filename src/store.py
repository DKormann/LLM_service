#%%
import flask
import json

json_data = []

class Store:
  """file storage"""
  def put_file():
    """Upload a pdf to the server.
    params: {"file": file, "path": str, "txt": str, "json": str}
    """
    file = flask.request.files['file']
    path = flask.request.form['path']
    txt = flask.request.form['txt']
    json = flask.request.form['json']

    json_data.append(json.loads(json))

    with open("store/"+path, 'wb') as f: f.write(file.read())
    with open("store/"+path+".txt", 'w') as f: f.write(txt)
    with open("store/index.json", 'w') as f: json.dump(json_data, f)

    return {"status": "success"}
  
  def list_files():
    """List the files in the store."""
    import os
    return {"files": os.listdir("store")}
  
  def get_file():
    """Download a file from the server."""

  