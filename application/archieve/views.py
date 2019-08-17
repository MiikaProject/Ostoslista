from flask import Blueprint,render_template,request,redirect,url_for
from flask_login import login_required,current_user
from datetime import date

from application import app, db

from application.archieve.models.Archieve import Archieve
from application.archieve.models.ArchieveItem import ArchieveItem

from application.archieve.forms.archieveitemform import ArchieveItemForm

#Create blueprint for arhieve
archieve = Blueprint('archieve',__name__,
                template_folder='templates')



@app.route("/archieve")
@login_required
def archieve_index():

    #Get user's groceryarchieve
    accountarchieve = Archieve.query.filter_by(account_id=current_user.id).first()
    if accountarchieve:
        archieveitems = accountarchieve.archieveitems 
    else:
        archieveitems=None

    if archieveitems:
        archieve_sum = Archieve.calculate_archieve_sum(accountarchieve.id)    
    else:
        archieve_sum=None

    #Calculate sum of items in archieve, method defined in archieve.models.arhieve.py
    

    return render_template("archieve.html",archieveitems=archieveitems,archieve_sum=archieve_sum)

#Remove item from archieve  
@archieve.route("/archieve/remove/<archieveitem_id>",methods=["POST"])
@login_required
def archieve_remove(archieveitem_id):

    #Get archieve for user
    accountarchieve = Archieve.query.filter_by(account_id=current_user.id).first()

    #Find selected item from archieveitems and remove it
    for archieveitem in accountarchieve.archieveitems:
        if archieveitem.id == int(archieveitem_id):
            accountarchieve.archieveitems.remove(archieveitem)
            db.session.add(accountarchieve)
            db.session.commit()

    return redirect(url_for("archieve_index"))   


#Edit buy date of archieve item
@archieve.route("/archieve/edit/<archieveitem_id>",methods=["POST","GET"])
@login_required
def archieve_edit(archieveitem_id):

    #Page for managing individual archieve item
    if(request.method=="GET"):
        requestedArchieveItem = ArchieveItem.query.filter(ArchieveItem.id==archieveitem_id).first()
        return render_template("archieveitem.html",archieveitem=requestedArchieveItem,form=ArchieveItemForm())

    #Handles edit request
    if(request.method=="POST"):

        #Pull form from request
        form = ArchieveItemForm(request.form)

        #Validates date: inserted date cannot be in the future and must be after 1.1.2000.Return back if fails and
        #display error message
        if not form.validate():
            requestedArchieveItem = ArchieveItem.query.filter(ArchieveItem.id==archieveitem_id).first()
            return(render_template("archieveitem.html",archieveitem=requestedArchieveItem,form=form))


        #Get edited archieve item from database and change date
        editedArchieveItem = ArchieveItem.query.filter(ArchieveItem.id==archieveitem_id).first()
        editedArchieveItem.date_bought=form.date.data
        db.session.add(editedArchieveItem)
        db.session.commit()
        
        return redirect(url_for("archieve_index"))