from flask import Blueprint, render_template
from flask.ext.login import current_user

from cookierun.models.routes import Route

main = Blueprint('main', __name__)

@main.route('/')
def main_screen():
    if current_user.is_authenticated():

        activities = Route.query.filter_by(user_id=current_user.get_id())

        stats = {'count': len(activities.all()),
                 'total_distance': sum([a.distance for a in activities.all()]),
                 'total_duration': sum([a.duration for a in activities.all()]),
                 'total_calories': sum([a.calories for a in activities.all()])}

        return render_template('main.html', stats=stats)
    else:
        return render_template('main.html')

