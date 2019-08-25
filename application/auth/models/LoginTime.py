#Database table for loginTime for account
from application import db

class LoginTime(db.Model):
    __tablename__='logintime'
    id = db.Column(db.Integer,primary_key=True)
    login_time= db.Column(db.DateTime, default=db.func.current_timestamp())
    account_id=db.Column(db.Integer,db.ForeignKey('account.id'))
    account = db.relationship('Account',back_populates='login_times')

    def __str__(self):
        return f'id:{self.id},time:{self.login_time}'