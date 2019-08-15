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
    

    #Aggregate query for calculating total price of items on grocerylist linked to account
    #Currently account only has 1 grocerylist attached to it, so there is no need to
    #deal with situations where one user would have multiple grocerylists. This
    #This might be a little silly way of doing this, maybe the method for calculating
    #sum should be inserted into either Account or Accountgrocerylist model instead of in grocerylist
    
    @staticmethod
    def calculate_grocerylist_sum(user_id):
        stmt = text("SELECT account.name,account.id,SUM(item.price) from account"
                    " INNER JOIN accountgrocerylist ON account.id = accountgrocerylist.account_id"
                    " INNER JOIN grocerylist ON accountgrocerylist.grocerylist_id = grocerylist.id"
                    " INNER JOIN groceryitem ON grocerylist.id = groceryitem.grocerylist_id"
                    " INNER JOIN item ON groceryitem.item_id = item.id"
                    " WHERE account.id=:user_id")
        result = db.engine.execute(stmt,user_id=user_id)
        sum = None
        for row in result:
            sum = row[2]

        return sum   