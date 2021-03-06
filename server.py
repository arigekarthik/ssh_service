import pysftp
import os
from flask import Flask, request, json
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/list_dir', methods=['GET'])
def list_remote_dir():
    sftp_conn = create_sftp_connection()
    directory_structure = sftp_conn.listdir_attr()
    dir_contents = []
    for attr in directory_structure:
        dir_contents.append([attr.filename, attr])
    sftp_conn.close()
    response = app.response_class(
        response=json.dumps(str(dir_contents)),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/upload', methods = ['POST'])
def upload_to_remote():
    f = request.files['file']
    f.save(f.filename)
    sftp_conn = create_sftp_connection()
    localFilePath = f"{f.filename}"
    remoteFilePath = f"{f.filename}"
    sftp_conn.put(localFilePath, remoteFilePath)
    sftp_conn.close()
    os.remove(f.filename)
    response = app.response_class(
        response=json.dumps({}),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/upload_from_string', methods = ['POST'])
def upload_to_remote_v2():
    body = request.get_json()
    with open("sftp_out.txt", "w") as text_file:
        text_file.write(body['file'])
    sftp_conn = create_sftp_connection()
    localFilePath = f"./sftp_out.txt"
    remoteFilePath = f"sftp_out.txt"
    sftp_conn.put(localFilePath, remoteFilePath)
    sftp_conn.close()
    os.remove("sftp_out.txt")
    response = app.response_class(
        response=json.dumps({}),
        status=200,
        mimetype='application/json'
    )
    return response

def create_sftp_connection():
    myHostname = "test.rebex.net"
    myUsername = "demo"
    myPassword = "password"
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    return pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts)

if __name__ == '__main__':
    app.run(port=5000)