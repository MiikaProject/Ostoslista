#Create database model for gloceries
from application import db

#Association table for GroceryList and Item, n to n relationship

grocerylistitems = db.Table('grocerylistitems',
    db.Column('grocerylist_id', db.Integer, db.ForeignKey('grocery_list.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id')),
    db.Column('id',db.Integer,primary_key=True)
)


#Database model for Grocery
class GroceryList(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(144),unique=True)
    items = db.relationship("Item",secondary=grocerylistitems,backref="grocerylists")

    def __init__(self,name):
        self.name = name
    
