from . import db
from flask_login import UserMixin
from sqlalchemy.sql import text

class User(UserMixin):
    def __init__(self, id):
        super().__init__()
        if id != "None":
            sql = text('''
                            SELECT id, username, password, role, visible
                            FROM "Users"
                            WHERE id=:id
                    ''')
            self.data = db.session.execute(sql, {"id":id}).fetchone()
            if self.data is not None:
                self.id = self.data[0]
                self.username = self.data[1]
                self.password = self.data[2]
                self.role = self.data[3]
                self.visible = self.data[4]
        else:
            self.data = None

    def is_active(self):
        return True
    
    def get_id(self):
        if self.data is not None:
            return self.id
        else:
            return None
    
    def is_authenticated(self):
        return super().is_authenticated
    
    def is_anonymous(self):
        return False
