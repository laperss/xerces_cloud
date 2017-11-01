#!/usr/bin/env python3
import os, shlex, random, string, binascii, shutil, zmq, sys, time
from flask import Flask, request, redirect, url_for, render_template, send_file, session
from subprocess import DEVNULL, STDOUT, call

ALLOWED_EXTENSIONS = set(['mkv'])
PUB_PORT = "5556"
SUB_PORT = "5557"
pub_context = zmq.Context()
pub_socket = pub_context.socket(zmq.PUB)
pub_socket.bind("tcp://*:%s" % PUB_PORT)
sub_context = zmq.Context()
sub_socket = sub_context.socket(zmq.PULL)
sub_socket.bind("tcp://*:%s" % SUB_PORT)

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
    if request.method == 'POST':
        input = request.files['file']
        if input and allowed_file(input.filename):
            # Saving input file
            filename, input_ext = os.path.splitext(input.filename)
            random_str = random_string()
            input_file = "input_%s.mkv" % (random_str)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_file)
            input.save(input_path)
            print("[local]\tSaving input file " + input_file + "...")

            # Publish task
            taskid = random.randint(0, 100)
            task = "task " + str(taskid)
            pub_socket.send_string(task)
            print("[send]\tPublish task (" + task + ") to workers...")

            # Wait for response
            res = sub_socket.recv()
            data = res.split()
            vmip = res.split()[3].decode("utf-8")
            print("[recv]\tReceive response (" + res.decode("utf-8") + ") from " + vmip + "...")

            # Delegate task
            vm = "vm " + str(vmip) + " file " + input_file
            pub_socket.send_string(vm)
            print("[send]\tDelegate task (" + vm + ") to " + vmip + "...")
            print("[send]\tSend file to worker...")
            os.system("scp -i /home/ubuntu/xerces_keypair.pem " + input_path +
                      " ubuntu@" + vmip + ":/home/ubuntu/")
            done = "done"
            pub_socket.send_string(done)
            print("[send]\tNotify file transfer complete...")

            # Wait for converted file
            time.sleep(30)
            session['output_path'] = "/home/ubuntu/" + filename + ".avi"

            # Delete input file
            print("[local]\tDeleting input file " + input_file + "...")
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
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

