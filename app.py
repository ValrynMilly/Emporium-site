import numpy as np
import os
import CVS as htm
from pathlib import Path
from flask import Flask, flash
from flask import render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'ESRGAN/LR'
DOWNLOAD_FOLDER = 'ESRGAN/results'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey' #<------- HIDE THIS IN ENV VARIABLES
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

def delete_files_in_directory(directory_path):
   try:
     files = os.listdir(directory_path)
     for file in files:
       file_path = os.path.join(directory_path, file)
       if os.path.isfile(file_path):
         os.remove(file_path)
     print("All files deleted successfully.")
   except OSError:
     print("Error occurred while deleting files.")

def change_extension(file_path, new_extension):
    base_name, _ = os.path.splitext(file_path)
    new_file_path = base_name + "." + new_extension
    os.rename(file_path, new_file_path)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def landing():
    delete_files_in_directory(DOWNLOAD_FOLDER)
    delete_files_in_directory(UPLOAD_FOLDER)
    if request.method == 'POST':
    # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            os.chdir('ESRGAN/')
            os.system('python3 test.py')
            os.chdir('..')
            newname = Path(filename).stem
            name = newname + "_rlt.png"
            return redirect(url_for('download_file', name=name))
    return render_template('landing.html')

@app.route('/download_file/<name>')
def download_file(name):
    return send_from_directory(app.config["DOWNLOAD_FOLDER"], name, as_attachment=True)

@app.route('/video_feed', methods=['POST'])
def video_feed():
    if request.method == 'POST':
       htm.main()
       return redirect(url_for('landing'))