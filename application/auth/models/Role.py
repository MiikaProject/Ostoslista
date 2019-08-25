#Database table for user role, eg. regular user, admin, superuser.

from application import db

class Role(db.Model):
    __tablename__='role'
    id = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,unique=True)
    users = db.relationship('Account', secondary='user_roles',back_populates='roles')

    def __init__(self,name):
        #Get the id of the role we want to add to user
        self.name=name

    def __str__(self):
        return f'role_id:{self.id},role_name:{self.name}'