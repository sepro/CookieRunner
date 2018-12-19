from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView

from flask_login import current_user

from wtforms import PasswordField

from werkzeug.security import generate_password_hash

from datetime import datetime


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_administrator


class UserAdminView(ModelView):
    column_searchable_list = ('username',)
    column_sortable_list = ('username',)
    column_exclude_list = ('password_hash', 'reset_key', 'registered',)
    form_excluded_columns = ('password_hash', 'reset_key', 'registered',)
    form_edit_rules = ('username', 'email', 'is_admin', 'is_banned', 'password', )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_administrator

    def scaffold_form(self):
        form_class = super(UserAdminView, self).scaffold_form()
        form_class.password = PasswordField('Password')
        return form_class

    def create_model(self, form):
        model = self.model(form.username.data, form.password.data, form.email.data, reset_key='',
                           is_admin=form.is_admin.data, is_banned=form.is_banned.data, registered=datetime.now().replace(microsecond=0))
        form.populate_obj(model)
        self.session.add(model)
        self._on_model_change(form, model, True)
        self.session.commit()
        return True

    def update_model(self, form, model):
        form.populate_obj(model)
        if form.password.data:
            model.password_hash = generate_password_hash(form.password.data)
        self.session.add(model)
        self._on_model_change(form, model, False)
        self.session.commit()
        return True


class CookieAdminView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_administrator

    def create_model(self, form):
        model = self.model(form.name.data, form.calories.data, form.brand.data, form.website.data)
        form.populate_obj(model)
        self.session.add(model)
        self._on_model_change(form, model, True)
        self.session.commit()
        return True


class RunAdminView(ModelView):
    column_exclude_list = ('gpx',)

    can_create = False
    can_edit = False

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_administrator
