from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from flask.ext.login import current_user
from gpx.parser import GPXParser
from cookierun.models.runs import Run
from cookierun import db
from werkzeug.utils import secure_filename
import hashlib


import os
from datetime import datetime

upload = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = {'gpx'}


def allowed_file(filename):
    """
    check if a filename has the correct extentsion
    :param filename: filename to check
    :return: a boolean True if the filename is valid, false otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@upload.route('/', methods=['GET', 'POST'])
def upload_screen():
    """
    controller to handle file uploads, checks extension, parses the file and adds it to the database. Uploading the same
    file twice by the same user is not possible
    """
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filename)

            gpx_parser = GPXParser()
            gpx_parser.read(filename)

            hasher = hashlib.md5()
            with open(filename, 'rb') as content_file:
                hasher.update(content_file.read())

            with open(filename, 'r') as content_file:
                content = content_file.read()

            user_id = current_user.id if current_user.is_authenticated() else -1

            file_hash = hasher.hexdigest() + '_' + str(user_id)
            run_exists = Run.query.filter_by(file_key=file_hash).first()

            if run_exists is None:
                run = Run(hasher.hexdigest(),
                            gpx_parser.total_distance,
                            gpx_parser.total_calories(),
                            gpx_parser.average_speed,
                            gpx_parser.total_time,
                            content,
                            user_id,
                            datetime.now().replace(microsecond=0))

                db.session.add(run)
                db.session.commit()

                flash("Uploaded file !", "success")
                return redirect(url_for('runs.runs_view', run_id=run.id))
            else:
                return redirect(url_for('runs.runs_view', run_id=run_exists.id))
        else:
            flash("File type not supported, upload a GPX file", "danger")
            return redirect(url_for('upload.upload_screen'))

    return render_template('upload.html')

