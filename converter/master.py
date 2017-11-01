#!/usr/bin/env python3
import os, shlex, random, string, binascii, shutil, zmq, sys, time
from flask import Flask, request, redirect, url_for, render_template, send_file, session
from subprocess import DEVNULL, STDOUT, call

ALLOWED_EXTENSIONS = set(['mkv'])
PUB_PORT = "5556"
SUB_PORT = "5557"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'tmp'
app.config['SECRET_KEY'] =  binascii.hexlify(os.urandom(24))

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route("/", methods=['GET', 'POST'])
def main():
    pub_context = zmq.Context()
    pub_socket = pub_context.socket(zmq.PUB)
    pub_socket.bind("tcp://*:%s" % PUB_PORT)

    sub_context = zmq.Context()
    sub_socket = sub_context.socket(zmq.PULL)
    sub_socket.bind("tcp://*:%s" % SUB_PORT)

    taskid = 1
    if request.method == 'POST':
        input = request.files['file']
        if input and allowed_file(input.filename):
            _, input_ext = os.path.splitext(input.filename)
            random_str = random_string()
            input_file = "input_%s.mkv" % (random_str)

            # Saving input file
            print("Saving input file")
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_file)
            input.save(input_path)

            # Publish task
            task = "task " + str(taskid)
            pub_socket.send_string(task)
            print("sent: ", task)

            # Wait for response
            res = sub_socket.recv()
            data = res.split()
            vmid = int(data[3])
            print("recv: ", res.decode("utf-8"))

            # Delegate task
            vm = "vm " + str(vmid) + " file " + input_file
            pub_socket.send_string(vm)
            vm_ip = "192.168.50.8"
            os.system("scp -i /home/ubuntu/xerces_keypair.pem " + input_path +
                      " ubuntu@" + vm_ip + "/home/ubuntu/")
            print("sent: ", vm)
            taskid += 1

            # session['output_path'] = output_path

            # Delete input file
            print("Deleting input file")
            os.remove(input_path)

            return redirect(url_for('done'))
    return render_template('upload.html')

@app.route("/done", methods=['GET'])
def done():
    return render_template('done.html')

@app.route("/file", methods=['GET'])
def file():
    output_path = session['output_path']
    _, output_ext = os.path.splitext(output_path)
    return send_file(output_path, attachment_filename='converted%s' % output_ext, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

