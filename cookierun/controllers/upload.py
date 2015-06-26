from flask import Blueprint,current_app, render_template, request, redirect, url_for

from gpx.parser import GPXParser

from cookierun.models.routes import Route

from cookierun.database import db

from werkzeug.utils import secure_filename

import os

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

            with open(filename, 'r') as content_file:
                content = content_file.read()

            route = Route(filename,
                          gpx_parser.total_distance,
                          gpx_parser.total_calories(),
                          gpx_parser.average_speed,
                          gpx_parser.total_time,
                          content,
                          1)

            db.session.add(route)
            db.session.commit()

            # return redirect(url_for('routes.view', route_id=route.id))
            return redirect(url_for('routes.routes_view', route_id=route.id))

    return render_template('upload.html')


@upload.route('/config')
def config():
    return current_app.config['UPLOAD_FOLDER']
