from application import db
from sqlalchemy.sql import text

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
    

    @staticmethod
    def calculate_grocerylist_sum(user_id):
        stmt = text("SELECT grocerylist.id, SUM(item.price)"
                    " FROM grocerylist"
                    " INNER JOIN groceryitem ON grocerylist.id = groceryitem.grocerylist_id"
                    " INNER JOIN item ON groceryitem.item_id = item.id"
                    " WHERE grocerylist.id=:user_id")
        result = db.engine.execute(stmt,user_id=user_id)
        
        sum = None
        for row in result:
            sum = row[1]

        return sum   