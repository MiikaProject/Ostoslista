from application import db
from sqlalchemy.sql import text
from decimal import Decimal

#Database model for Archieve which collects users purchases

class Archive(db.Model):
    __tablename__='archive'
    id = db.Column(db.Integer,primary_key=True)
    account_id = db.Column(db.Integer,db.ForeignKey('account.id'))
    account = db.relationship("Account",uselist=False,back_populates="archive")
    archiveitems = db.relationship("ArchiveItem",back_populates="archive")

    def __str__(self):
        return f'id:{self.id},linkedaccount:{self.account},archieveitems:{self.archiveitems}'



    #Aggregate query for calculating tota sum of items on archieve
    @staticmethod
    def calculate_archive_sum(archive_id):
        archive_sum = None

        stmt = text("SELECT archive.id,SUM(item.price) from archive"
                    " INNER JOIN archiveitem ON archive.id=archiveitem.archive_id"
                    " INNER JOIN item ON archiveitem.item_id=item.id"
                    " GROUP BY archive.id"
                    " HAVING archive.id=:archive_id")

        result = db.engine.execute(stmt,archive_id=archive_id)

        #Get sum from result
        for row in result:
            archive_sum = row[1]

        #round to 2 decimals
        archive_sum = Decimal(archive_sum).quantize(Decimal("1.00"))
        return archive_sum
