import pysftp
from flask import Flask, json
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
    return dir_contents

if __name__ == '__main__':
    app.run(port=5000)