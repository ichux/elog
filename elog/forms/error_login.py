from flask_wtf import FlaskForm  # type: ignore
from wtforms import PasswordField, StringField  # type: ignore
from wtforms.validators import DataRequired  # type: ignore

# from wtforms.validators import DataRequired, Length, Email

# from elog.forms import Unique
# from elog.models.authenticate import User
#
#
# class EmailPasswordForm(FlaskForm):
#     uniqueness = Unique(User, User.username, message='There is already an account with that email.')
#     email = StringField('Email', validators=[DataRequired(), Email(), uniqueness])
#     password = PasswordField('Password', validators=[DataRequired()])


class ErrorLoginUserForm(FlaskForm):
    username = StringField(
        "username", [DataRequired("Username is required")]
    )  # , Length(min=4, max=25)
    password = PasswordField(
        "password", [DataRequired("Password is required")]
    )  # , Length(min=6, max=200)
