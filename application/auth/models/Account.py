from application import db

#Database model for user account
class Account(db.Model):

    __tablename__ = "account"
  
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False,unique=True)
    password = db.Column(db.String(144), nullable=False)
    account_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    login_times = db.relationship("LoginTime",back_populates="account")
    accountgrocerylists =db.relationship("AccountGrocerylist",back_populates="account")
    archieve = db.relationship("Archieve",uselist=False,back_populates="account")
    roles = db.relationship('Role', secondary='user_roles',back_populates='users')

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def is_super(self):
        super = False
        for role in self.roles:
            if role.name == 'super':
                super = True
        return super        
    
    def is_admin(self):
        admin = False
        for role in self.roles:
            if role.name == 'admin':
                admin = True
        return admin 

    def is_user(self):
        user = False
        for role in self.roles:
            if role.name == 'user':
                user = True
        return user

    def has_role(self,role_needed):
        
        access = False
        for role in self.roles:
            if role.name == role_needed:
                access = True
        return access        

    def highest_role(self):
        if(self.is_super()):
            return 'super'
        if(self.is_admin()):
            return 'admin'
        return 'user'    

    def __str__(self):
        return f'name:{self.name},username:{self.username},grocerylists:{self.accountgrocerylists},roles:{self.roles}'
        