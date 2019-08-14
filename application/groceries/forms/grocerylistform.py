from flask_wtf import FlaskForm
from wtforms import StringField

#GroceryForm for adding new grocerylist
class GroceryListForm(FlaskForm):
    name = StringField("Name")
    class meta:
        csrf=False