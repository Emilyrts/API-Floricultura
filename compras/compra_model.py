from datetime import datetime

from clientes.cliente_model import Cliente
from config import db


class Compra(db.Model):
    __tablename__ = "compras"
    
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    itens = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    cliente = db.relationship("Cliente", backref="compras")

    def __init__(self, data, valor_total, cliente_id, itens, status):
        self.data = data
        self.valor_total = valor_total
        self.cliente_id = cliente_id
        self.itens = itens
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "data": self.data.strftime("%Y-%m-%d"),
            "valor_total": self.valor_total,
            "cliente_id": self.cliente_id,
            "cliente_nome": self.cliente.nome if self.cliente else None,
            "itens": self.itens,
            "status": self.status,
        }