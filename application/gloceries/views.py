from flask import Blueprint,Flask,render_template,request,redirect,url_for
from application import app, db
from application.items.models import Item
from application.gloceries.models import GroceryList

groceries = Blueprint('groceries',__name__,
                template_folder='templates')

@groceries.route("/groceries",methods=["GET"])
def groceries_index():

    #Get all groceries from database
    grocerylist = GroceryList.query.all()[0].items

    return render_template("groceries.html",grocerylist=grocerylist)

@groceries.route("/groceries/new_grocery",methods=["GET"])
def grocery_form():

    #Get all possible item choices from database
    itemlist = Item.query.distinct(Item.name).all()
    return render_template("new_grocery.html",itemlist=itemlist)

@groceries.route("/groceries/remove/<grocery_id>",methods=["POST"])
def groceries_remove(grocery_id):
    #Get grocerylist items
    groceries = GroceryList.query.all()[0]
    #convert grocery_id to int
    grocery_id = int(grocery_id)
    
    #Look for item in groceries.items and remove it from list
    for item in groceries.items:

        if item.id==grocery_id:
            groceries.items.remove(value=item)

    #Commit change to database
    db.session.add(groceries)
    db.session.commit()

    return redirect(url_for("groceries.groceries_index"))


@groceries.route("/groceries",methods=["POST"])
def groceries_create():

    #Pull name from request form
    addedItem = request.form.get("name")

    #Get item from database
    itemToBeAdded = Item.query.filter(Item.name==addedItem).first() 

    #Get grocerylist from database
    groceries = GroceryList.query.all()[0]

    #This block deals with cases where grocerylist already contains 
    #the item added to grocerylist. Unfortunately this block has no functionality yet,
    # because there were issues with the way this block initially worked. The attemped solution was
    #to create a new item object to be added to the grocerieslist. This solution caused 
    #duplicate to be formed in the Items datatable which is not expected behavior. This 
    #might have something to do with decralaring the association table in groceries/models as 
    #SQLalchemy table instead of actual Model. Possible fix to this issue could be creating a actual
    #model of the association table and adding the item directly to the association table instead of 
    #working with the SQLalchemy reference to groceries thing... Solving this issue is top priority. 
    #Due to time being trying to add same items to the grocerylist twice leads to redirect back.
    #

    if itemToBeAdded  in groceries.items:
        return redirect(url_for("groceries.grocery_form"))


    #Deals with cases where added item is not yet on grocerylist, adds
    #item to the grocerylist.
    else:  
        groceries.items.append(itemToBeAdded )
        db.session.add(groceries)
        db.session.commit()


    return redirect(url_for("groceries.grocery_form"))


