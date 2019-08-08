from flask import Blueprint,render_template,request,redirect,url_for
from flask_login import login_required

from application import app, db
from application.items.models.item import Item
from application.items.forms.itemform import ItemForm

items = Blueprint('items',__name__,
                template_folder='templates')


@items.route("/items",methods=["GET"])
@login_required
def items_index():

    #Pull all items from database and order them aplhabetically
    itemlist = Item.query.order_by(Item.name).all()

    return render_template("items.html",itemlist=itemlist,form=ItemForm()) 


@items.route("/items", methods=["POST"])
@login_required
def item_create():
    #Get form
    form = ItemForm(request.form)

    #Get name
    name = (form.name.data)

    #Get price
    price = form.price.data

     #Run validations described in itemform.py, if false return and display errors
    if not form.validate():
        itemlist = Item.query.order_by(Item.name).all()
        form.name.data=""
        form.price.data=['']
        return render_template("items.html",itemlist=itemlist,form=form)

    #Add Item to database
    newItem = Item(name=name,price=price)
    db.session().add(newItem)
    db.session().commit()

    return redirect(url_for("items.items_index"))

@items.route("/items/<item_id>",methods=["GET"])
@login_required
def item_view(item_id):
    item = Item.query.filter(Item.id==item_id).first()
    return render_template("item.html",item=item,form=ItemForm())   

@items.route("/items/<item_id>",methods=["POST"])
@login_required
def item_update(item_id):
    form = ItemForm(request.form)
    print(form)
    #get new name and price from form
    name = form.name.data
    price = form.price.data
    print(price)
    #get item from database
    item = Item.query.filter(Item.id==item_id).first()

    #set new name and price, check for empty fields, in that case keep old values
    if(name!=""):
        item.name=name
    if not price:
        print(price)
    else:
        item.price=price    

    #commit changes to database
    db.session.add(item)
    db.session.commit()

    return redirect(url_for("items.items_index"))

@items.route("/items/remove/<item_id>",methods=["POST"])
@login_required
def item_remove(item_id):
    #get item from database
    item = Item.query.filter(Item.id==item_id).first()

    #remove item from database
    db.session.delete(item)
    db.session.commit()


    return redirect(url_for("items.items_index"))