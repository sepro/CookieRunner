from flask import Blueprint
from flask import render_template

from cookierun.models.cookies import Cookie

cookie = Blueprint('cookie', __name__)

@cookie.route('/cookies')
def cookies_list():
    return render_template('cookies.html')

@cookie.route('/cookies/view/<id>')
def cookies_view(id):
    cookie = Cookie.query.get_or_404(id)
    return 'Cookie ' + cookie.name

