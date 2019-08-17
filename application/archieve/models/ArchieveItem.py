from application import db

# Association table between Archieve and Item, n to n relationship
class ArchieveItem(db.Model):
    __tablename__='archieveitem'
    id = db.Column(db.Integer,primary_key=True)
    item_id = db.Column(db.Integer,db.ForeignKey('item.id'))
    archieve_id = db.Column(db.Integer,db.ForeignKey('archieve.id'))
    date_bought=db.Column(db.Date,default=db.func.current_date())
    item = db.relationship("Item",back_populates="archieveitem")
    archieve = db.relationship("Archieve",back_populates="archieveitems")
    


    def __str__(self):
        return f'id: {self.id}, item_id:{self.item_id},item:{self.item},archieve:{self.archieve},date:{self.date_bought}'