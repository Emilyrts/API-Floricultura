from config import db


class ItemModel(db.Model):
    __tablename__ = "itens"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    compra_id = db.Column(db.Integer, nullable=False)  # assumindo que existe tabela de compras
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    valor_unitario = db.Column(db.Float, nullable=False)
    
    produto = db.relationship("Produto", backref="itens")

    def __init__(self, compra_id, produto_id, quantidade, valor_unitario):
        self.compra_id = compra_id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.valor_unitario = valor_unitario

    def to_json(self):
        return {
            "id": self.id,
            "compra_id": self.compra_id,
            "produto_id": self.produto_id,
            "quantidade": self.quantidade,
            "valor_unitario": self.valor_unitario
        }

    @classmethod
    def find_by_id(cls, id_item):
        return cls.query.get(id_item)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
