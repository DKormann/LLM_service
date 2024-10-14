#%%
import flask
import json

json_data = []

with open("store/index.json", 'r') as f: json_data = json.load(f)

class Store:
  """file storage"""

  def put_file():
    """Upload a pdf to the server.
    params: {"uuid": str, "file": file, "txt": str, "json": str}
    """
    file = flask.request.files['file']
    uuid = flask.request.form['uuid']
    txt = flask.request.form['txt']
    json = flask.request.form['json']

    data = json.loads(json)
    data['uuid'] = uuid
    json_data.append(json.loads(json))

    with open("store/"+uuid+".pdf", 'wb') as f: f.write(file.read())
    with open("store/"+uuid+".txt", 'w') as f: f.write(txt)
    with open("store/index.json", 'w') as f: json.dump(json_data, f)

    return {"status": "success"}

  def get_files(offset = 0, min_date:int = None, max_date:int = None, searchterm = None):
    """List the files in the store maximum 50.
    params: {"offset": int= 0, "min_date": str= None, "max_date": str= None}
    """
    filtered = json_data
    if min_date: filtered = [x for x in filtered if x['date'] >= min_date]
    if max_date: filtered = [x for x in filtered if x['date'] <= max_date]

    return {"files": filtered[offset:offset+50]}

  def get_file(uuid: str):
    """Download a file from the server."""
    return flask.send_file("store/"+uuid+".pdf")



