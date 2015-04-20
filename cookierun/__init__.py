from flask import Flask
from cookierun.controllers.main import main


app = Flask(__name__)
app.register_blueprint(main)
