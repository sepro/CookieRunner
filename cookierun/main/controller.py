from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def home_screen():
    return 'Hello World'

