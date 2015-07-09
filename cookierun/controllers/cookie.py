from flask import Blueprint, render_template, jsonify

from cookierun.models.cookies import Cookie
from math import floor

cookies = Blueprint('cookies', __name__)


@cookies.route('/')
def cookies_list():
    """
    shows a list of all the cookies in the database
    """
    all_cookies = Cookie.query.all()
    return render_template("cookies.html", cookies=all_cookies)

@cookies.route('/view/<cookie_id>')
def cookies_view(cookie_id):
    """
    shows the details of one cookie
    """
    cookie = Cookie.query.get_or_404(cookie_id)
    return render_template("cookies.html", cookie=cookie)

@cookies.route('/count/<calories>')
def cookies_count(calories):
    """
    function to check how many of each cookie you can eat while staying within the desired limit of calories

    :param calories: the total number of calories allowed
    :return: a json object with all the cookies and how many you can eat staying within the limits
    """
    output = {}
    all_cookies = Cookie.query.all()
    for cookie in all_cookies:
        output[cookie.name] = floor(float(calories)/float(cookie.calories))
    return jsonify(output)
