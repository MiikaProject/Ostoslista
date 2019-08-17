from flask import Blueprint,Flask,render_template,request,redirect,url_for
from flask_login import login_required,current_user

from application import app, db
#Database models
from application.items.models.item import Item
from application.groceries.models.GroceryList import GroceryList
from application.groceries.models.GroceryItem import GroceryItem
from application.auth.models.AccountGrocerylist import AccountGrocerylist
from application.archieve.models.Archieve import Archieve
from application.archieve.models.ArchieveItem import ArchieveItem
#Forms
from application.groceries.forms.groceryform import GroceryForm
from application.groceries.forms.grocerylistform import GroceryListForm


#Create blueprint for the moodule
groceries = Blueprint('groceries',__name__,
                template_folder='templates')


@groceries.route("/groceries",methods=["GET"])
@login_required
def groceries_index():

    #Get all possible item choices from database
    itemlist = Item.query.all()

    #Get grocerylist for currently logged in user
    lists = AccountGrocerylist.query.filter_by(account_id=current_user.id).all()

    #If user has multiple grocerylists, collect them all, in the current version user is
    #only assumed to have one grocerylist!
    grocerylists = []
    for accountgrocerylist in lists:
        grocerylists.append(accountgrocerylist.grocerylist)
    
    #Chooce the first grocerylist to be the grocerylist to be shown
    if grocerylists:
        grocerylist = grocerylists[0] 
    else:
        grocerylist = None
    
    #Calculate total cost of groceries on grocerylist by using aggregate query
    #defined in groceries.GroceryList
    sum = GroceryList.calculate_grocerylist_sum(current_user.id)

    return render_template("/groceries.html",grocerylist=grocerylist,itemlist=itemlist,form=GroceryForm(),sum=sum)
    
        

@groceries.route("/groceries/remove/<grocery_id>",methods=["POST"])
@login_required
def groceries_remove(grocery_id):
    #Get matching grocerylist for logged in user
    accountgrocerylists = AccountGrocerylist.query.filter_by(account_id=current_user.id).all()
    #Current version only supports 1 grocerylist so choose that
    accountgrocerylist = accountgrocerylists[0].grocerylist

    #Get groceryarchieve for logged in user
    accountarchieve = Archieve.query.filter_by(account_id=current_user.id).first()
    print(accountarchieve)
    newArchieveItem = ArchieveItem()
    print(newArchieveItem)


    #convert grocery_id to int
    grocery_id = int(grocery_id)

    #Look for item in groceries.items and remove it from list
    for grocery in accountgrocerylist.items:
        if grocery.id==grocery_id:
            accountgrocerylist.items.remove(grocery)
            newArchieveItem.item=grocery.item
            accountarchieve.archieveitems.append(newArchieveItem)

    #Commit change to database
    print(accountarchieve)
    db.session.add(accountgrocerylist)
    db.session.add(accountarchieve)
    db.session.commit()

    return redirect(url_for("groceries.groceries_index"))


@groceries.route("/groceries",methods=["POST"])
@login_required
def groceries_create():
    
    #Pull name from form
    form = GroceryForm(request.form)
    addedItem = form.name.data

    #Get item from database
    itemToBeAdded = Item.query.filter(Item.name==addedItem).first() 

    #If item is not on itemlist,return back to groceries page and display error
    if not itemToBeAdded:
        #Add error message
        errorlist=list(form.name.errors)
        errorlist.append('Item not on Itemlist!')
        form.name.errors=tuple(errorlist)
        #Reset textfield
        form.name.data=""
        #Get itemlist for page
        itemlist=Item.query.all()
        #Get grocerylist for user
        accountgrocerylist = AccountGrocerylist.query.filter_by(account_id=current_user.id).first()
        grocerylist=accountgrocerylist.grocerylist
        return render_template("groceries.html",grocerylist=grocerylist,form=form,itemlist=itemlist)

    #Add item to grocerylist
    else:
        #Get grocerylist for currently logged in user

        accountgrocerylists = AccountGrocerylist.query.filter_by(account_id=current_user.id).all()

        #Current version assumes user only has 1 grocerylist so chooce it
        accountgrocerylist = accountgrocerylists[0].grocerylist

        #Create a new instance of groceryitem and add it to grocerylist    
        groceryitem=GroceryItem()
        groceryitem.item= itemToBeAdded
        accountgrocerylist.items.append(groceryitem)
        db.session.add(accountgrocerylist)
        db.session.commit()

        return redirect(url_for("groceries.groceries_index"))


@groceries.route("/groceries/lists/new", methods=["GET","POST"])
@login_required
def grocerylists_new():

    #Display the page which allows user to create grocerylist
    if request.method=="GET":
        return(render_template("grocerylists.html",form=GroceryListForm()))

    #Handle creation of grocerylist for user
    elif request.method=="POST":
        form = GroceryListForm(request.form)
        name = form.name.data

        accountlist = AccountGrocerylist()
        grocerylist =GroceryList(name)
        accountlist.account = current_user
        grocerylist.accounts.append(accountlist)
        db.session.add(grocerylist)
        db.session.commit()

        return redirect(url_for("groceries.groceries_index"))
