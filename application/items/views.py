from flask import Blueprint,render_template,request,redirect,url_for
from application import app, db
from application.items.models.item import Item

items = Blueprint('items',__name__,
                template_folder='templates')


@items.route("/items",methods=["GET"])
def items_index():

    #Pull all items from database and order them aplhabetically
    itemlist = Item.query.order_by(Item.name).all()

    return render_template("items.html",itemlist=itemlist) 


@items.route("/items", methods=["POST"])
def item_create():
    #Pull name from request
    name = (request.form.get("name"))

    #Convert text into float and deal with possible usage of "," as decimal pointer
    price = (request.form.get("price"))
    price = price.replace(",",".")
    price = float(price)

    #Add Item to database
    newItem = Item(name=name,price=price)
    db.session().add(newItem)
    db.session().commit()

    return redirect(url_for("items.items_index"))

@items.route("/items/<item_id>",methods=["GET"])
def item_view(item_id):
    item = Item.query.filter(Item.id==item_id).first()
    return render_template("item.html",item=item)   

@items.route("/items/<item_id>",methods=["POST"])
def item_update(item_id):
    #get new name and price from form
    name = request.form.get("name")
    price = (request.form.get("price"))
    
    #get item from database
    item = Item.query.filter(Item.id==item_id).first()

    #set new name and price, check for empty fields, in that case keep old values
    if(name!=""):
        item.name=name
    if(price!=""):
        price = price.replace(",",".")
        item.price=float(price)

    #commit changes to database
    db.session.add(item)
    db.session.commit()

    return redirect(url_for("items.items_index"))

@items.route("/items/remove/<item_id>",methods=["POST"])
def item_remove(item_id):
    #get item from database
    item = Item.query.filter(Item.id==item_id).first()

    #remove item from database
    db.session.delete(item)
    db.session.commit()


    return redirect(url_for("items.items_index"))