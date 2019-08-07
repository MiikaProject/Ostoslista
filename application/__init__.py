from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Flask
app = Flask(__name__)

import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URL")
else:
    # SQLAlchemy configuration
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///groceries.db"
    app.config["SQLALCHEMY_ECHO"]=True


#Create secret key
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
try:
    db.create_all()
except:
    pass    


    