from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os

#Create Flask app
app = Flask(__name__)
Bootstrap(app)

#SQL-Alchemy configurations for Heroku and local use
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///groceries.db"
    app.config["SQLALCHEMY_ECHO"]=False


#Create secret key
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

db = SQLAlchemy(app)

#Import database models
from application.items.models.item import Item
from application.groceries.models.GroceryList import GroceryList
from application.groceries.models.GroceryItem import GroceryItem
from application.auth.models.Account import Account
from application.auth.models.AccountGrocerylist import AccountGrocerylist
from application.archieve.models.Archieve import Archieve
from application.archieve.models.ArchieveItem import ArchieveItem

#Import blueprints(=views), blueprints allow modular project structure in Flask applications
from application.main.views import main
from application.items.views import items
from application.groceries.views import groceries
from application.auth.views import auth
from application.archieve.views import archieve

#Register blueprints
app.register_blueprint(items)
app.register_blueprint(main)
app.register_blueprint(groceries)
app.register_blueprint(auth)
app.register_blueprint(archieve)

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
try:
    db.create_all()
except:
    pass    


    