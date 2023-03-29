from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, password, nome, tipo):
        self.id = id
        self.email = email
        self.password = password
        self.nome = nome
        self.tipo = tipo