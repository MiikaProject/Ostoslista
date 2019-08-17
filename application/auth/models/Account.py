from application import db


#Database model for user account
class Account(db.Model):

    __tablename__ = "account"
  
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False,unique=True)
    password = db.Column(db.String(144), nullable=False)
    accountgrocerylists =db.relationship("AccountGrocerylist",back_populates="account")
    archieve = db.relationship("Archieve",uselist=False,back_populates="account")

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True


    def __str__(self):
        return f'name:{self.name},username:{self.username},grocerylists:{self.accountgrocerylists}'    