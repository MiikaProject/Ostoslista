from flask import Flask

#Flask
app = Flask(__name__)


# SQLAlchemy configuration
from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///groceries.db"
app.config["SQLALCHEMY_ECHO"]=True
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

db = SQLAlchemy(app)

#Import database models
from application.items.models.item import Item
from application.groceries.models.GroceryList import GroceryList
from application.groceries.models.GroceryItem import GroceryItem
from application.auth.models.Account import Account

#Import blueprints(=routes=views)
from application.main.views import main
from application.items.views import items
from application.groceries.views import groceries
from application.auth.views import auth

#Register blueprints
app.register_blueprint(items)
app.register_blueprint(main)
app.register_blueprint(groceries)
app.register_blueprint(auth)

#Configure login manager
from flask_login import LoginManager
login_manager=LoginManager()
login_manager.init_app(app)

login_manager.login_view="auth.auth_login"
login_manager.login_message="Please login to use this page."

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(user_id)


#Create database tables
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


Accounts = Account.query.all()
if not Accounts:
    defaultuser = Account(name="default",username="default",password="salasana") 
    db.session.add(defaultuser)
    db.session.commit()       
