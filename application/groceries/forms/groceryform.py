from flask_wtf import FlaskForm
from wtforms import StringField

#GroceryForm for adding new grocery to grocerylist
class GroceryForm(FlaskForm):
    name = StringField("Name")
    class meta:
        csrf=False



        