from flask import Blueprint,render_template,request,redirect,url_for
from application import app, db
from application.items.models.item import Item

items = Blueprint('items',__name__,
                template_folder='templates')


@items.route("/new_item")
def items_form():
    return render_template("new_item.html") 

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