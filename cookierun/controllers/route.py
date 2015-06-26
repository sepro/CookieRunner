from flask import Blueprint
from flask import render_template

from cookierun.models.routes import Route


routes = Blueprint('routes', __name__)

@routes.route('/test/')
def test():
    return "TEST OK"

@routes.route('/view/<route_id>')
def routes_view(route_id):
    route = Route.query.get_or_404(route_id)
    return render_template('routes.html', route=route)
