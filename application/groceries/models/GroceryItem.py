
from application import db

# Association table between Grocerylist and Item, n to n relationship
class GroceryItem(db.Model):
    __tablename__='groceryitem'
    id = db.Column(db.Integer,primary_key=True)
    item_id = db.Column(db.Integer,db.ForeignKey('item.id'))
    grocerylist_id = db.Column(db.Integer,db.ForeignKey('grocerylist.id'))
    item = db.relationship("Item",back_populates="groceryitem")
    grocerylist = db.relationship("GroceryList",back_populates="items")


    def __str__(self):
        return f'id: {self.id}, item_id:{self.item_id},item:{self.item},grocerylist_id:{self.grocerylist_id},grocerylist={self.grocerylist}'