from flask import Blueprint,Flask,render_template,request,redirect,url_for
from flask_login import login_user,logout_user

from application import app, db
from application.auth.models.Account import Account
from application.auth.forms.loginform import LoginForm


#Create blueprint for the moodule
auth = Blueprint('auth',__name__,
                template_folder='templates')

@auth.route("/auth/login",methods=["GET","POST"])
def auth_login():

    #If method is post, return login page    
    if request.method=="GET":
        return render_template("login.html",form=LoginForm())

    #If method is post verify credentials and log user in or display error message    
    elif request.method=="POST":
        form=LoginForm(request.form)

        #Get username and password
        username=form.username.data
        password=form.password.data

        #Try to find user from database
        user = Account.query.filter_by(username=username,password=password).first()
        
        #User not valid
        if not user:
                form.username.data=""
                return render_template("login.html", form = form,
                               error = "No such username or password")
        
        #User valid                             
        else:
                login_user(user)
                return redirect(url_for("main.index"))


#Handles logout request                
@auth.route("/auth/logout")
def auth_logout():
        logout_user()
        return redirect(url_for("main.index"))  