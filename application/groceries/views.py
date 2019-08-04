from flask import Blueprint,Flask,render_template,request,redirect,url_for
from application import app, db
from application.items.models.item import Item
from application.groceries.models.GroceryList import GroceryList
from application.groceries.models.GroceryItem import GroceryItem

#Create blueprint for the moodule
groceries = Blueprint('groceries',__name__,
                template_folder='templates')


@groceries.route("/groceries",methods=["GET"])
def groceries_index():

    #Get all groceries from database for speficic list

    grocerylist = GroceryList.query.filter_by(name='default').first()

    #Collect individual items from groceryitems
    items = []
    for groceryitem in grocerylist.items:
        items.append(groceryitem.item)
        print(groceryitem)

    return render_template("/groceries.html",grocerylist=grocerylist.items)

@groceries.route("/groceries/new_grocery",methods=["GET"])
def grocery_form():

    #Get all possible item choices from database
    itemlist = Item.query.all()

    return render_template("new_grocery.html",itemlist=itemlist)

@groceries.route("/groceries/remove/<grocery_id>",methods=["POST"])
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
def groceries_create():
    #Pull name from request form
    addedItem = request.form.get("name")

    #Get item from database
    itemToBeAdded = Item.query.filter(Item.name==addedItem).first() 

    #If item is not on itemlist,return back to add new grocery page
    if not itemToBeAdded:
        return redirect(url_for("groceries.grocery_form"))

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

        return redirect(url_for("groceries.grocery_form"))


