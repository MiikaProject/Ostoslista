from application import db
from sqlalchemy.sql import text
from decimal import Decimal

#Database model for GroceryList
class GroceryList(db.Model):
    __tablename__ = 'grocerylist'
    id = db.Column(db.Integer,primary_key=True)
    account_id = db.Column(db.Integer,db.ForeignKey('account.id'))
    items = db.relationship("GroceryItem",back_populates="grocerylist")
    account = db.relationship("Account",uselist=False,back_populates="grocerylist")

    
    def __str__(self):
        return f'id:{self.id},items:{self.items},owner:{self.account.name}'
    

    #Aggregate query for calculating total price of items on grocerylist linked to account
    #Currently account only has 1 grocerylist attached to it, so there is no need to
    #deal with situations where one user would have multiple grocerylists. This
    #This might be a little silly way of doing this, maybe the method for calculating
    #sum should be inserted into either Account or Accountgrocerylist model instead of in grocerylist

    @staticmethod
    def calculate_grocerylist_sum(user_id):
        stmt = text("SELECT account_id,SUM(item.price) FROM Grocerylist"
                    " INNER JOIN groceryitem ON grocerylist_id=grocerylist.id"
                    " INNER JOIN item ON item_id=item.id"
                    " GROUP BY grocerylist.id"
                    " HAVING account_id=:user_id")
        result = db.engine.execute(stmt,user_id=user_id)
        sum = None

        #Get result and round it to 2 decimals
        for row in result:
            sum = row[1]
            sum = Decimal(sum).quantize(Decimal("1.00"))

        return sum   