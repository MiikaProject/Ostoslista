#Association table for account and grocerylist

from application import db

class AccountGrocerylist(db.Model):
    __tablename__='accountgrocerylist'
    id = db.Column(db.Integer,primary_key=True)
    account_id = db.Column(db.Integer,db.ForeignKey('account.id'))
    grocerylist_id = db.Column(db.Integer,db.ForeignKey('grocerylist.id'))
    account = db.relationship("Account",back_populates="accountgrocerylists")
    grocerylist = db.relationship("GroceryList",back_populates="accounts")


    def __str__(self):
        return f'id:{self.id},grocerylist:{self.grocerylist},account:{self.account}'