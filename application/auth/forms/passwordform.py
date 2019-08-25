from flask_wtf import FlaskForm
from wtforms import PasswordField,validators

#Form for account page for changing password
class PasswordForm(FlaskForm):
    oldpassword=PasswordField("Old Password")
    newpassword=PasswordField('New password',[validators.Length(min=3)])
    repeatedpassword=PasswordField('Repeat new password',[validators.Length(min=3)])
    class Meta:
        csrf=False