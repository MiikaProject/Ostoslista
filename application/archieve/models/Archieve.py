from application import db
from sqlalchemy.sql import text
from decimal import Decimal

#Database model for Archieve which collects users purchases

class Archieve(db.Model):
    __tablename__='archieve'
    id = db.Column(db.Integer,primary_key=True)
    account_id = db.Column(db.Integer,db.ForeignKey('account.id'))
    account = db.relationship("Account",uselist=False,back_populates="archieve")
    archieveitems = db.relationship("ArchieveItem",back_populates="archieve")

    def __str__(self):
        return f'id:{self.id},linkedaccount:{self.account},archieveitems:{self.archieveitems}'



    #Aggregate query for calculating tota sum of items on archieve
    @staticmethod
    def calculate_archieve_sum(archieve_id):
        archieve_sum = None

        stmt = text("SELECT archieve.id,SUM(item.price) from archieve"
                    " INNER JOIN archieveitem ON archieve.id=archieveitem.archieve_id"
                    " INNER JOIN item ON archieveitem.item_id=item.id"
                    " GROUP BY archieve.id"
                    " HAVING archieve.id=archieve_id")

        result = db.engine.execute(stmt,archieve_id=archieve_id)

        #Get sum from result
        for row in result:
            archieve_sum = row[1]

        #round to 2 decimals
        archieve_sum = Decimal(archieve_sum).quantize(Decimal("1.00"))
        return archieve_sum
