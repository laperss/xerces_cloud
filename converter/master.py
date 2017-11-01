#!/usr/bin/env python3
import os, shlex, random, string, binascii, shutil
from flask import Flask, request, redirect, url_for, render_template, send_file, session
from subprocess import DEVNULL, STDOUT, call

ALLOWED_EXTENSIONS = set(['mkv'])

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

def convert_video(source, dest):
    cmd = """mencoder %s -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=3000
             -oac copy -o %s""" % (source, dest)
    print("Converting video file")
    call(shlex.split(cmd), stdout=DEVNULL, stderr=STDOUT)

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        input = request.files['file']
        if input and allowed_file(input.filename):
            _, input_ext = os.path.splitext(input.filename)
            random_str = random_string()
            input_name = "input_%s" % (random_str)

            # Saving input file
            print("Saving input file")
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_name + input_ext)
            input.save(input_path)
            
            # Convert file
            output_name = "output_%s" % (random_str)
            output_ext = '.avi'
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_name + output_ext)
            convert_video(input_path, output_path)
            session['output_path'] = output_path

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

