from flask import Blueprint,render_template
from flask_login import current_user
from application.auth.utils import role_required

#Create blueprint for main
main = Blueprint('main',__name__,
                template_folder='templates')

#Application's main page 
              
@main.route("/")
def index():
    return render_template("index.html")