from application import db

#Database model for GroceryList
class GroceryList(db.Model):
    __tablename__ = 'grocerylist'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(144))
    items = db.relationship("GroceryItem",back_populates="grocerylist")
    accounts = db.relationship("AccountGrocerylist",back_populates="grocerylist")

    def __init__(self,name):
        self.name = name
    
    def __str__(self):
        return f'listname:{self.name},items:{self.items},owners:{self.accounts}'
    
