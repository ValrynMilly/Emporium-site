import numpy as np
import time
import os
import CVS as htm
from flask import Flask
from flask import render_template, Response, request, redirect, url_for, send_from_directory
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
import glob

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey' #<------- HIDE THIS IN ENV VARIABLES
app.config['UPLOAD_FOLDER'] = 'ESRGAN\ESRGAN\LR'
app.config['DOWNLOAD_FOLDER'] = 'ESRGAN\ESRGAN/results'

files = glob.glob('ESRGAN/LR/')

class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")

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

directory_path = 'ESRGAN\ESRGAN\LR'  
directory_path2 = 'ESRGAN\ESRGAN/results'
cwd = os.getcwd()


def download_files_in_directory(directory_path2):
     files_in = os.listdir(directory_path2)[0]
     send_from_directory(directory_path2, files_in, as_attachment=True)


@app.route("/", methods=['GET', "POST"])
@app.route("/home", methods=['GET', "POST"])
def landing():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        os.chdir('ESRGAN\ESRGAN/')
        os.system('python test.py')
        os.chdir('..')
        os.chdir('..')
        download_files_in_directory(directory_path2)
        delete_files_in_directory(directory_path)
        delete_files_in_directory(directory_path2)
    return render_template('landing.html', form=form)


@app.route('/video_feed', methods=['POST'])
def video_feed():
    if request.method == 'POST':
       htm.main()
       return redirect(url_for('landing'))