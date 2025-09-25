from config import db


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    rg = db.Column(db.String(20), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)

    def __init__(self, nome, rg, telefone, endereco):
        self.nome = nome
        self.rg = rg
        self.telefone = telefone
        self.endereco = endereco

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'rg': self.rg,
            'telefone': self.telefone,
            'endereco': self.endereco
        }