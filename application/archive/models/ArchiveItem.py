from application import db

# Association table between Archieve and Item, n to n relationship
class ArchiveItem(db.Model):
    __tablename__='archiveitem'
    id = db.Column(db.Integer,primary_key=True)
    item_id = db.Column(db.Integer,db.ForeignKey('item.id'))
    archive_id = db.Column(db.Integer,db.ForeignKey('archive.id'))
    date_bought=db.Column(db.Date,default=db.func.current_date())
    item = db.relationship("Item",back_populates="archiveitem")
    archive = db.relationship("Archive",back_populates="archiveitems")
    


    def __str__(self):
        return f'id: {self.id}, item_id:{self.item_id},item:{self.item},archieve:{self.archive},date:{self.date_bought}'