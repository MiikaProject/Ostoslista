from flask_wtf import FlaskForm
from wtforms import PasswordField,StringField

#Form for login page
class LoginForm(FlaskForm):
    username=StringField("Username")
    password=PasswordField("Password")

    class Meta:
        csrf=False