from flask_wtf import FlaskForm
from wtforms import StringField

class GroceryForm(FlaskForm):
    name = StringField("Name")
    class meta:
        csrf=False



        