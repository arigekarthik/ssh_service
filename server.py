import pysftp
import os
from flask import Flask, request, json
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/list_dir', methods=['GET'])
def list_remote_dir():
    response = app.response_class(
        response=json.dumps(connect_and_list()),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/upload', methods = ['POST'])
def upload_to_remote():
    f = request.files['file']
    f.save(f.filename)
    sftp_conn = create_sftp_connection()
    localFilePath = f"./{f.filename}"
    remoteFilePath = f"./{f.filename}"
    sftp_conn.put(localFilePath, remoteFilePath)
    sftp_conn.close()
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

def connect_and_list():
    myHostname = "test.rebex.net"
    myUsername = "demo"
    myPassword = "password"
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    dir_contents = []
    with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts) as sftp:
        print("Connection succesfully stablished ... ")
        directory_structure = sftp.listdir_attr()
        for attr in directory_structure:
            dir_contents.append([attr.filename, attr])
    return str(dir_contents)

if __name__ == '__main__':
    app.run(port=5000)