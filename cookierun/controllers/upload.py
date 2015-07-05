from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from flask.ext.login import current_user
from gpx.parser import GPXParser
from cookierun.models.routes import Route
from cookierun.database import db
from werkzeug.utils import secure_filename
import hashlib


import os
from datetime import datetime

upload = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = {'gpx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@upload.route('/', methods=['GET', 'POST'])
def upload_screen():
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
            route_exists = Route.query.filter_by(file_key=file_hash).first()

            if route_exists is None:
                route = Route(hasher.hexdigest(),
                              gpx_parser.total_distance,
                              gpx_parser.total_calories(),
                              gpx_parser.average_speed,
                              gpx_parser.total_time,
                              content,
                              user_id,
                              datetime.now().replace(microsecond=0))

                db.session.add(route)
                db.session.commit()

                flash("Uploaded file !", "success")
                return redirect(url_for('routes.routes_view', route_id=route.id))
            else:
                return redirect(url_for('routes.routes_view', route_id=route_exists.id))

    return render_template('upload.html')

