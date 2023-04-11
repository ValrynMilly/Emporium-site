import numpy as np
import time
import os
import CVS as htm
from flask import Flask
from flask import render_template, Response, request, redirect, url_for
app = Flask(__name__)

@app.route("/")
def landing():
    return render_template('landing.html')


@app.route('/video_feed', methods=['POST'])
def video_feed():
    if request.method == 'POST':
       htm.main()
       return redirect(url_for('landing'))
   
   
