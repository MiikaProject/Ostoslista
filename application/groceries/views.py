from flask import Blueprint,Flask,render_template,request,redirect,url_for
from flask_login import login_required,current_user

from application import app, db
from application.auth.utils import role_required

#Database models
from application.items.models.item import Item
from application.groceries.models.GroceryList import GroceryList
from application.groceries.models.GroceryItem import GroceryItem
from application.archive.models.Archive import Archive
from application.archive.models.ArchiveItem import ArchiveItem
#Forms
from application.groceries.forms.groceryform import GroceryForm
from application.groceries.forms.grocerylistform import GroceryListForm


#Create blueprint for the moodule
groceries = Blueprint('groceries',__name__,
                template_folder='templates')


@groceries.route("/groceries",methods=["GET"])
@login_required
@role_required('user')
def groceries_index():

    #Get all possible item choices from database
    itemlist = Item.query.all()

    #Get grocerylist for currently logged in user
    grocerylist = GroceryList.query.filter_by(account_id=current_user.id).first()

    print(grocerylist)
    
    #Calculate total cost of groceries on grocerylist by using aggregate query
    #defined in groceries.GroceryList
    sum = GroceryList.calculate_grocerylist_sum(current_user.id)

    return render_template("/groceries.html",grocerylist=grocerylist,itemlist=itemlist,form=GroceryForm(),sum=sum)
    
        

@groceries.route("/groceries/remove/<grocery_id>",methods=["POST"])
@login_required
def groceries_remove(grocery_id):
    #Get matching grocerylist for logged in user
    grocerylist = GroceryList.query.filter_by(account_id=current_user.id).first()

    #convert grocery_id to int
    grocery_id = int(grocery_id)

    #Look for item in groceries.items and remove it from list
    for grocery in grocerylist.items:
        if grocery.id==grocery_id:
            grocerylist.items.remove(grocery)

    #Commit change to database
    db.session.add(grocerylist)
    db.session.commit()

    return redirect(url_for("groceries.groceries_index"))

@groceries.route("/groceries/buy/<grocery_id>",methods=["POST"])
def grocerylist_buy(grocery_id):
    #Get matching grocerylist for logged in user
    grocerylist = GroceryList.query.filter_by(account_id=current_user.id).first()

    #Get groceryarchieve for logged in user
    accountarchive = Archive.query.filter_by(account_id=current_user.id).first()
    newArchiveItem = ArchiveItem()


    #convert grocery_id to int
    grocery_id = int(grocery_id)

    #Look for item in groceries.items and remove it from list
    for grocery in grocerylist.items:
        if grocery.id==grocery_id:
            grocerylist.items.remove(grocery)
            newArchiveItem.item=grocery.item
            accountarchive.archiveitems.append(newArchiveItem)

    #Commit change to database
    db.session.add(grocerylist)
    db.session.add(accountarchive)
    db.session.commit()

    return redirect(url_for("groceries.groceries_index"))

@groceries.route("/groceries/list/<item_id>",methods=["POST"])
def grocerylist_add(item_id):
    print(item_id)
    itemToBeAdded = Item.query.filter(Item.id==item_id).first()
    print(itemToBeAdded)
    #Get grocerylist for currently logged in user

    grocerylist = GroceryList.query.filter_by(account_id=current_user.id).first()

    #Create a new instance of groceryitem and add it to grocerylist    
    groceryitem=GroceryItem()
    groceryitem.item= itemToBeAdded
    grocerylist.items.append(groceryitem)
    db.session.add(grocerylist)
    db.session.commit() 

    return redirect(url_for("groceries.groceries_index"))

