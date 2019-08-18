from flask import Blueprint,Flask,render_template,request,redirect,url_for
from flask_login import login_user,logout_user
from sqlalchemy import exc

from application import app, db
from application.auth.models.Account import Account
from application.auth.forms.loginform import LoginForm
from application.auth.forms.registerform import RegisterForm

from application.auth.models.Account import Account
from application.archieve.models.Archieve import Archieve


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

#Register page and also the functionality to add new account to database        
@auth.route("/auth/register",methods=["GET","POST"])
def auth_register():
        
        if request.method=="GET":        
                return(render_template("register.html",form=RegisterForm()))

        elif request.method=="POST":
                #Collect information from registerform
                form=RegisterForm(request.form)
                name=form.name.data
                username=form.username.data
                password=form.password.data

                #Return back to register page if validations fail
                if not form.validate():
                        return(render_template("register.html",form=form))
                
                #Create new account to be added to database. Also create a grocery archieve for account.
                newAccount = Account(name,username,password)
                archieveForAccount = Archieve()
                newAccount.archieve=archieveForAccount

                #Try to enter account into database
                try:
                        db.session.add(newAccount)
                        db.session.commit()

                #Deal with situation if username is already taken by returning to register page and displaying error message.SQLite and POSTGre use
                #differente errors messages, check for both.
                except exc.SQLAlchemyError as error:
                        error=str(error.orig)
                        print(error)   
                        if error=="UNIQUE constraint failed: account.username":
                                form.username.data=""
                                return(render_template("register.html",form=form,error="Username not available, pick another one!"))
                        elif error=='duplicate key value violates unique constraint "account_username_key"':
                                form.username.data=""
                                return(render_template("register.html",form=form,error="Username not available, pick another one!"))
                        else:
                                return(redirect(url_for('auth.auth_login')))
                return(redirect(url_for('auth.auth_login')))