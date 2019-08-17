# Form for editing archieveitem

from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import validators,ValidationError
from datetime import date

#Form for login page
class ArchieveItemForm(FlaskForm):
    date=DateField("Date")

    #Validate date, cant be in the future and must be after 1.1.2000
    def validate_date(form,field):
        datadate=form.date.data
        maxdate = date.today()
        mindate = date(year=2000,month=1,day=1)
        if(maxdate<datadate):
            raise ValidationError('Your from the future,right?')
        if(mindate>datadate):
            raise ValidationError('Purschase must be done before 1.1.2000')        


    class Meta:
        csrf=False