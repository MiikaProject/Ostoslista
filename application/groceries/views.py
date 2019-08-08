from flask import Blueprint,Flask,render_template,request,redirect,url_for
from flask_login import login_required

from application import app, db
from application.items.models.item import Item
from application.groceries.models.GroceryList import GroceryList
from application.groceries.models.GroceryItem import GroceryItem
from application.groceries.forms.groceryform import GroceryForm

#Create blueprint for the moodule
groceries = Blueprint('groceries',__name__,
                template_folder='templates')


@groceries.route("/groceries",methods=["GET"])
@login_required
def groceries_index():

    #Get all possible item choices from database
    itemlist = Item.query.all()

    #Get all groceries from database for speficic list
    grocerylist = GroceryList.query.filter_by(name='default').first()

    #Collect individual items from groceryitems, if possible 
    items = []
    if grocerylist:
        if grocerylist.items:
            for groceryitem in grocerylist.items:
                items.append(groceryitem.item)
                return render_template("/groceries.html",grocerylist=grocerylist.items,itemlist=itemlist,form=GroceryForm())
        else:
            return render_template("/groceries.html",itemlist=itemlist,form=GroceryForm())
    else:
        return render_template("/groceries.html",itemlist=itemlist,form=GroceryForm())
    
        

@groceries.route("/groceries/remove/<grocery_id>",methods=["POST"])
@login_required
def groceries_remove(grocery_id):
    #Get matching grocerylist
    grocerylist = GroceryList.query.filter_by(name='default').first()

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
        return render_template("groceries.html",form=form,itemlist=itemlist)

    #Add item to grocerylist
    else:
        #Get grocerylist from database
        grocerylist = GroceryList.query.filter_by(name='default').first()

        #Create a new instance of groceryitem and add it to grocerylist    
        groceryitem=GroceryItem()
        groceryitem.item= itemToBeAdded
        grocerylist.items.append(groceryitem)
        db.session.add(grocerylist)
        db.session.commit()

        return redirect(url_for("groceries.groceries_index"))


