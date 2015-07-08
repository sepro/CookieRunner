from flask import Blueprint, render_template, flash, redirect, url_for
from flask.ext.login import current_user

from cookierun.models.routes import Route

routes = Blueprint('routes', __name__)

@routes.route('/')
def routes_list():
    if not current_user.is_authenticated():
        flash("You are not permitted to view this !", "danger")
        return redirect(url_for('main.main_screen'))
    else:
        if current_user.is_admin:
            all_routes = Route.query.all()
            return render_template('routes.html', routes=all_routes)
        else:
            flash("You are not permitted to view this !", "danger")
            return redirect(url_for('main.main_screen'))


@routes.route('/view/<route_id>')
def routes_view(route_id):
    route = Route.query.get_or_404(route_id)
    if str(route.user_id) == current_user.get_id() or route.user_id == -1:
        return render_template('routes.html', route=route)
    else:
        flash("You are not permitted to view this run !", "danger")
        return redirect(url_for('main.main_screen'))


@routes.route('/user/')
def routes_user():
    user_routes = Route.query.filter_by(user_id=current_user.get_id()).all()
    return render_template('routes.html', routes=user_routes)
