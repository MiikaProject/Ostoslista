from flask import Blueprint,Flask,render_template,request,redirect,url_for
from flask_login import login_user,logout_user,login_required,current_user
from sqlalchemy import exc
from datetime import datetime

from application import app, db
from application.auth.utils import role_required
from application.auth.models.Account import Account
from application.auth.forms.loginform import LoginForm
from application.auth.forms.registerform import RegisterForm
from application.auth.forms.passwordform import PasswordForm
from application.auth.forms.removeform import RemoveForm

from application.auth.models.Account import Account
from application.archieve.models.Archieve import Archieve
from application.auth.models.Role import Role
from application.auth.models.UserRoles import UserRoles
from application.auth.models.LoginTime import LoginTime


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
                newLogin = LoginTime()
                user.login_times.append(newLogin)
                db.session.add(user)
                db.session.commit()
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

                #Add role User to new account
                
                wantedRole = Role.query.filter_by(name='user').first()
                newAccount.roles.append(wantedRole)
                print(newAccount)

                #Try to enter account into database
                try:
                        db.session.add(newAccount)
                        db.session.commit()

                #Deal with situation if username is already taken by returning to register page and displaying error message.SQLite and POSTGre use
                #differente errors messages, check for both.
                except exc.SQLAlchemyError as error:
                        error=str(error.orig)
                        print('error',error)   
                        if error=="UNIQUE constraint failed: account.username":
                                form.username.data=""
                                return(render_template("register.html",form=form,error="Username not available, pick another one!"))
                        elif error=='duplicate key value violates unique constraint "account_username_key"':
                                form.username.data=""
                                return(render_template("register.html",form=form,error="Username not available, pick another one!"))
                        else:
                                return(redirect(url_for('auth.auth_login')))
                return(redirect(url_for('auth.auth_login')))

#Admin panel view

@auth.route("/auth/admin")
@login_required
@role_required('admin')
def auth_admin():
        #Get all accounts and pass it to the admin page
        accounts = Account.query.all()
        return(render_template("admin.html",accounts=accounts))


#Admin can remove basic users accounts
@auth.route("/auth/user/remove/<account_id>",methods=["POST"])
@login_required
@role_required('admin')
def admin_remove_user(account_id):
        print(account_id)
        removedUser= Account.query.filter_by(id=account_id).first()

        #Basic users only have one role which is user, this is to make sure admin cant remove admin 
        if len(removedUser.roles) == 1:
                db.session.delete(removedUser)
                db.session.commit()
                return redirect(url_for('auth.auth_admin'))
        return redirect(url_for('auth.auth_admin'))



#Page which is shown if user tries to see page his/her role is not authorized to see
@auth.route("/auth/unauthorized/<role>")    
def auth_unauthorized(role):
        return render_template('unauthorized.html',role=role)


#Page for managing user account
@auth.route("/auth/account/<user_id>")
@login_required
@role_required('user')
def auth_account(user_id):
        return render_template('account.html',user_id=user_id,passwordform=PasswordForm())

#Remove account
@auth.route("/auth/account/remove/<account_id>",methods=["POST"])
@login_required
@role_required('user')
def account_remove(account_id):
        password = (request.form["password"])
        #Check if password matches and account match, then delete account and return to main or return to account page with error message
        if(password==current_user.password and current_user.id==int(account_id)):
                deletedAccount = Account.query.filter_by(id=account_id).first()
                db.session.delete(deletedAccount)
                db.session.commit()
        else: 
                return render_template('account.html',user_id=account_id,passwordform=PasswordForm(),removeerror='Password wrong!')          
        
        return redirect(url_for('main.index'))


#Change password
@auth.route("/auth/account/password/<account_id>",methods=["POST"])
@login_required
@role_required('user')
def password_change(account_id):
        form = PasswordForm(request.form)
 
        if (form.oldpassword.data == current_user.password):
                print('right pw')
                if(form.repeatedpassword.data==form.newpassword.data):
                        print('match')
                        if not form.validate():
                                print('short pw')
                                return render_template('account.html',user_id=account_id,passwordform=form,error='Password mininum lenght is 3!')

                        current_user.password=form.newpassword.data
                        print(current_user.password)
                        db.session.add(current_user)
                        db.session.commit()
                else:
                        print('wrong match')
                        return render_template('account.html',user_id=account_id,passwordform=form,error='New passwords do not match!')

        else:
                return render_template('account.html',user_id=account_id,passwordform=form,error='Incorrect password!')
        

        return render_template('account.html',user_id=account_id,passwordform=form,error='Password changed!')       