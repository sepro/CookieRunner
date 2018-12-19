from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required

from cookierun.models.runs import Run

runs = Blueprint('runs', __name__)

@runs.route('/')
@login_required
def runs_list():
    """
    shows a list of all routes in the database, only admins are allowed to see this
    """
    if current_user.is_admin:
        all_runs = Run.query.all()
        return render_template('runs.html', runs=all_runs)
    else:
        flash("You are not permitted to view this !", "danger")
        return redirect(url_for('main.main_screen'))


@runs.route('/view/<run_id>')
def runs_view(run_id):
    """
    detailed view of one run, only the user that uploaded the run can see it. Anonymously uploaded files are
    visible to all
    :param run_id: the ID of the route to show
    """
    run = Run.query.get_or_404(run_id)
    if str(run.user_id) == current_user.get_id() or run.user_id == -1:
        return render_template('runs.html', run=run)
    else:
        flash("You are not permitted to view this run !", "danger")
        return redirect(url_for('main.main_screen'))


@runs.route('/user/')
def runs_user():
    """
    shows a list of all runs from the current user
    """
    user_runs = Run.query.filter_by(user_id=current_user.get_id()).all()
    return render_template('runs.html', runs=user_runs)
