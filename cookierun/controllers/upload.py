from flask import Blueprint
from flask import current_app, render_template, request
from gpx.parser import GPXParser

from werkzeug.utils import secure_filename

import os

upload = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = {'gpx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@upload.route('/upload', methods=['GET', 'POST'])
def upload_screen():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filename)

            gpx_parser = GPXParser()
            gpx_parser.read(filename)

            return "Uploaded " + filename + "\nCalories " + str(gpx_parser.total_calories()) + "\nDistance " \
                   + str(gpx_parser.total_distance)
    return render_template('upload.html')


@upload.route('/upconfig')
def upconfig():
    return current_app.config['UPLOAD_FOLDER']
