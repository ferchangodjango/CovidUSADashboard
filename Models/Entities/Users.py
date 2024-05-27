from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self,id,user,password) -> None:
        self.id=id
        self.user=user
        self.password=password
    @classmethod
    def checkPassword(self,cryptopassword,password):
        return check_password_hash(cryptopassword,password)

