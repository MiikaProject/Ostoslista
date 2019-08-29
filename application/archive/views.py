from flask import Blueprint,render_template,request,redirect,url_for
from flask_login import login_required,current_user
from datetime import date

from application import app, db

from application.archive.models.Archive import Archive
from application.archive.models.ArchiveItem import ArchiveItem

from application.archive.forms.archiveitemform import ArchiveItemForm

#Create blueprint for arhieve
archive = Blueprint('archive',__name__,
                template_folder='templates')



@app.route("/archive")
@login_required
def archive_index():

    #Get user's groceryarchive
    accountarchive = Archive.query.filter_by(account_id=current_user.id).first()
    if accountarchive:
        archiveitems = accountarchive.archiveitems 
    else:
        archiveitems=None

    if archiveitems:
        archive_sum = Archive.calculate_archive_sum(accountarchive.id)    
    else:
        archive_sum=None

    #Calculate sum of items in archieve, method defined in archieve.models.arhieve.py
    

    return render_template("archive.html",archiveitems=archiveitems,archive_sum=archive_sum)

#Remove item from archieve  
@archive.route("/archive/remove/<archiveitem_id>",methods=["POST"])
@login_required
def archive_remove(archiveitem_id):

    #Get archieve for user
    accountarchive = Archive.query.filter_by(account_id=current_user.id).first()

    #Find selected item from archieveitems and remove it
    for archiveitem in accountarchive.archiveitems:
        if archiveitem.id == int(archiveitem_id):
            accountarchive.archiveitems.remove(archiveitem)
            db.session.add(accountarchive)
            db.session.commit()

    return redirect(url_for("archive_index"))   


#Edit buy date of archieve item
@archive.route("/archive/edit/<archiveitem_id>",methods=["POST","GET"])
@login_required
def archive_edit(archiveitem_id):

    #Page for managing individual archieve item
    if(request.method=="GET"):
        requestedArchiveItem = ArchiveItem.query.filter(ArchiveItem.id==archiveitem_id).first()
        return render_template("archiveitem.html",archiveitem=requestedArchiveItem,form=ArchiveItemForm())

    #Handles edit request
    if(request.method=="POST"):

        #Pull form from request
        form = ArchiveItemForm(request.form)

        #Validates date: inserted date cannot be in the future and must be after 1.1.2000.Return back if fails and
        #display error message
        if not form.validate():
            requestedArchiveItem = ArchiveItem.query.filter(ArchiveItem.id==archiveitem_id).first()
            return(render_template("archiveitem.html",archiveitem=requestedArchiveItem,form=form))


        #Get edited archieve item from database and change date
        editedArchieveItem = ArchiveItem.query.filter(ArchiveItem.id==archiveitem_id).first()
        editedArchieveItem.date_bought=form.date.data
        db.session.add(editedArchieveItem)
        db.session.commit()
        
        return redirect(url_for("archive_index"))