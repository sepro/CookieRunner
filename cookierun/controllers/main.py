from flask import Blueprint
from flask import render_template

main = Blueprint('main', __name__)

@main.route('/')
def main_screen():
    return render_template('main.html')

