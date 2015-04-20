from flask import Blueprint
from flask import render_template

cookie = Blueprint('cookie', __name__)

@cookie.route('/cookies')
def cookies_list():
    return render_template('cookies.html')

