from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

from cookierun.database import db
from cookierun.loginmanager import login_manager
from cookierun.admin import MyAdminIndexView, UserAdminView, CookieAdminView, RouteAdminView

from cookierun.controllers.main import main
from cookierun.controllers.cookie import cookies
from cookierun.controllers.route import routes
from cookierun.controllers.upload import upload
from cookierun.controllers.auth import auth

from cookierun.models.users import User
from cookierun.models.cookies import Cookie
from cookierun.models.routes import Route

app = Flask(__name__)

db = SQLAlchemy(app)

app.register_blueprint(main)
app.register_blueprint(cookies, url_prefix='/cookies')
app.register_blueprint(routes, url_prefix='/routes')
app.register_blueprint(upload, url_prefix='/upload')
app.register_blueprint(auth, url_prefix='/auth')

db.create_all()

admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(UserAdminView(User, db.session))
admin.add_view(CookieAdminView(Cookie, db.session))
admin.add_view(RouteAdminView(Route, db.session))

login_manager.init_app(app)
login_manager.login_view = 'login'

