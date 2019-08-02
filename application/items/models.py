#Create database model for Item
from application import db

class Item(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(144))
    price = db.Column(db.Float)

    def __init__(self,name,price):
        self.name = name
        self.price = price  

