from flask import Flask

#Flask
app = Flask(__name__)


# SQLAlchemy configuration
from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///groceries.db"
app.config["SQLALCHEMY_ECHO"]=False

db = SQLAlchemy(app)

#Import database models
from application.items.models.item import Item
from application.groceries.models.GroceryList import GroceryList
from application.groceries.models.GroceryItem import GroceryItem

#Import blueprints(=routes=views)
from application.main.views import main
from application.items.views import items
from application.groceries.views import groceries

#Register blueprints
app.register_blueprint(items)
app.register_blueprint(main)
app.register_blueprint(groceries)



db.create_all()

#Initializing grocerylist for testing
Testgrocery = GroceryList.query.all()
if not Testgrocery:
    NewGroceryList = GroceryList("default")
    db.session.add(NewGroceryList)
    db.session.commit()

#Initialize some test Items.
Itemlist = Item.query.all()
if not Itemlist:
    item1 = Item(name="Viili",price=0.7)
    item2 = Item(name="Mehukeitto",price=1.4)
    item3 = Item(name="Banaani",price=0.2)
    item4 = Item(name="Maito",price=0.65)
    item5 = Item(name="Appelsiini",price=0.5)
    items =[item1,item2,item3,item4,item5]
    for item in items:
        db.session.add(item)
    db.session.commit()    
