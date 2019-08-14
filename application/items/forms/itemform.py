from flask_wtf import FlaskForm
from wtforms import StringField,validators,DecimalField,fields

#Form for adding item to itemlist


#Create custom field to make field work even if user uses comma or dot
class FlexibleDecimalField(fields.DecimalField):

    def process_formdata(self, valuelist):
        if valuelist:
            valuelist[0] = valuelist[0].replace(",", ".")
        return super(FlexibleDecimalField, self).process_formdata(valuelist)       

class ItemForm(FlaskForm):
    name = StringField("Name",[validators.Length(min=3)])
    price = FlexibleDecimalField("Price",[validators.NumberRange(min=0)])
    class meta:
        csrf=False

    