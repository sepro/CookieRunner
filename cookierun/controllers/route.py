from flask import Blueprint
from flask import render_template

from cookierun.models.routes import Route


routes = Blueprint('routes', __name__)

@routes.route('/')
def routes_list():
    all_routes = Route.query.all()
    return render_template('routes.html', routes=all_routes)


@routes.route('/view/<route_id>')
def routes_view(route_id):
    route = Route.query.get_or_404(route_id)
    return render_template('routes.html', route=route)
