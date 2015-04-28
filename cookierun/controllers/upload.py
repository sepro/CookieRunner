from flask import Blueprint
from flask import current_app, render_template, request, redirect, url_for

from werkzeug import secure_filename

import os

upload = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = set(['gpx'])

def allowed_file(filename):
    return '.' in filename and \
               filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@upload.route('/upload', methods=['GET', 'POST'])
def upload_screen():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return "Uploaded " + filename
    return render_template('upload.html')

@upload.route('/upconfig')
def upconfig():
  return current_app.config['UPLOAD_FOLDER']
