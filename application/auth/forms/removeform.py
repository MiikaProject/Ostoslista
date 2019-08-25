from flask_wtf import FlaskForm
from wtforms import PasswordField,StringField

#Form for account page for removing account
class RemoveForm(FlaskForm):
    password=PasswordField("Password")

    class Meta:
        csrf=False