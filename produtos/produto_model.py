from config import db

class Produto(db.Model):
    __tablename__ = "produtos"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    
    tipo_id = db.Column (db.Integer, db.ForeignKey("tipos.id"), nullable=False)
    tipo = db.relationship("Tipo", backref="produtos")
    
    def __init__ (self, nome, quantidade, preco, tipo_id):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
        self.tipo_id = tipo_id
        
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'quantidade': self.quantidade,
            'preco': self.preco,
            'tipo_id': self.tipo_id
        }
        
class ProdutoNaoEncontrado(Exception):
    pass

@classmethod
def find_by_id(cls, id_produto):
    return cls.query.get(id_produto)
    
def produto_por_id(id_produto):
    produto = Produto.query.get(id_produto)
    if not produto:
        raise ProdutoNaoEncontrado(f"Produto não encontrado.")
    return produto.to_dict()

def listar_produtos():
    produtos = Produto.query.all()
    return [produto.to_dict() for produto in produtos]

def adicionar_produto(novos_dados):
    from tipo.tipo_model import Tipo
    
    tipo = Tipo.query.get(novos_dados['tipo_id'])
    if tipo is None:
        return {"message":"Esse tipo não existe."}, 404
    
    novo_produto = Produto(
        nome = novos_dados['nome'],
        quantidade = float(novos_dados['quantidade']),
        tipo_id = int(novos_dados['tipo_id'])
    )
    
    db.session.add(novo_produto)
    db.session.commit()
    return {"message": "Produto adicionado com sucesso!"}, 201

def atualizar_produto(id_produto, novos_dados):
    produto = Produto.query.get(id_produto)
    if not produto:
        raise ProdutoNaoEncontrado(f"Produto não encontrado.")
    
    produto.nome = novos_dados['nome']
    produto.quantidade = float(novos_dados['quantidade'])
    produto.tipo_id = int(novos_dados['tipo_id'])
    
    db.session.commit()
    return {"message": f"Produto atualizado com sucesso!"}

def excluir_produto(id_produto):
    produto = Produto.query.get(id_produto)
    if not produto:
        raise ProdutoNaoEncontrado(f"Produto não encontrado.")
    
    db.session.delete(produto)
    db.session.commit()
    