#Database model for Item
from application import db

class Item(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(144))
    price = db.Column(db.Float)
    groceryitem = db.relationship("GroceryItem",back_populates="item")
    archieveitem = db.relationship("ArchieveItem",back_populates="item")

    def __init__(self,name,price):
        self.name = name
        self.price = price 

    def __str__(self):
        return f'{self.name},{self.price},{self.groceryitem}'

