from flask import Blueprint
from flask import render_template

from cookierun.models.routes import Route


routes = Blueprint('routes', __name__)

@routes.route('/view/<route_id>')
def cookies_view(route_id):
    route = Route.query.get_or_404(route_id)
    return render_template('routes.html', route=route)
