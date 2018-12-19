from flask import Blueprint, render_template
from flask_login import current_user

from cookierun.models.runs import Run

main = Blueprint('main', __name__)


@main.route('/')
def main_screen():
    """
    Shows the main screen, if a user is logged in an overview is shown. Otherwise a link to the upload section
    """
    if current_user.is_authenticated:

        activities = Run.query.filter_by(user_id=current_user.get_id())

        total_duration = sum([a.duration for a in activities.all()])
        hours = str(int(total_duration//3600))
        minutes = str(int((total_duration % 3600)//60)).rjust(2, '0')
        seconds = str(int(total_duration % 60)).rjust(2, '0')

        stats = {'count': len(activities.all()),
                 'total_distance': sum([a.distance for a in activities.all()]),
                 'total_hours': hours,
                 'total_minutes': minutes,
                 'total_seconds': seconds,
                 'total_calories': sum([a.calories for a in activities.all()])}

        return render_template('main.html', stats=stats)
    else:
        return render_template('main.html')

