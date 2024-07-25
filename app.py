import numpy as np
import time
import os
import CVS as htm
from flask import Flask
from flask import render_template, Response, request, redirect, url_for, send_from_directory, send_file
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
import glob

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey' #<------- HIDE THIS IN ENV VARIABLES
app.config['UPLOAD_FOLDER'] = 'ESRGAN\LR'
app.config['DOWNLOAD_FOLDER'] = 'ESRGAN/results'


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

directory_path = 'ESRGAN\LR'  
directory_path2 = 'ESRGAN/results/'
cwd = os.getcwd()
file_td = os.listdir('ESRGAN/results')[0]

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def landing():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        os.chdir('ESRGAN/')
        os.system('python test.py')
        os.chdir('..')
        #delete_files_in_directory(directory_path)
        redirect("/download")
        #delete_files_in_directory(directory_path2)
    return render_template('landing.html', form=form)

@app.route("/download",methods=["GET","POST"])
def download():
    if request.method=="GET":
        return render_template("landing.html")
    elif request.method=="POST":
        return send_from_directory(directory_path2, file_td, as_attachment=True)

@app.route('/video_feed', methods=['POST'])
def video_feed():
    if request.method == 'POST':
       htm.main()
       return redirect(url_for('landing'))