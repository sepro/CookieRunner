from flask import Blueprint, render_template, jsonify

from cookierun.models.cookies import Cookie
from math import floor

cookies = Blueprint('cookies', __name__)


@cookies.route('/')
def cookies_list():
    all_cookies = Cookie.query.all()
    return render_template("cookies.html", cookies=all_cookies)

@cookies.route('/view/<cookie_id>')
def cookies_view(cookie_id):
    cookie = Cookie.query.get_or_404(cookie_id)
    return render_template("cookies.html", cookie=cookie)

@cookies.route('/count/<calories>')
def cookies_count(calories):
    output = {}
    all_cookies = Cookie.query.all()
    for cookie in all_cookies:
        output[cookie.name] = floor(float(calories)/float(cookie.calories))
    return jsonify(output)
