from flask import Blueprint
from flask import render_template

from cookierun.models.cookies import Cookie


cookies = Blueprint('cookies', __name__)


@cookies.route('/')
def cookies_list():
    return render_template('cookies.html')


@cookies.route('/view/<cookie_id>')
def cookies_view(cookie_id):
    cookie = Cookie.query.get_or_404(cookie_id)
    return 'Cookie ' + cookie.name
