from config import db

class Tipo (db.Model):
    __tablename__= 'tipos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    
    def __init__ (self, nome):
        self.nome = nome
        
    def to_dict(self):
        return {'id': self.id, 'nome': self.nome}
    
class TipoNaoEncontrado(Exception):
    pass

def tipo_por_id(id_tipo):
    tipo = Tipo.query.get(id_tipo)
    if not tipo:
        raise TipoNaoEncontrado(f"Tipo não encontrado")
    return tipo.to_dict()

def listar_tipos():
    tipos = Tipo.query.all()
    return [tipo.to_dict() for tipo in tipos]

def adicionar_tipo(novos_dados):
    nome = novos_dados.get("nome")
    if not nome:
        return {'erro': 'Campo "nome" é obrigatório'}, 400
    
    novo_tipo = Tipo(
        nome=novos_dados['nome']
    )
    
    db.session.add(novo_tipo)
    db.session.commit()
    return {'message': 'Novo tipo de flor adicionado com sucesso!'}, 201

def atualizar_tipo(id_tipo, novos_dados):
        tipo = Tipo.query.get(id_tipo)
        if not tipo:
            raise TipoNaoEncontrado (f'Tipo de flor não encontrado.')
        
        nome_antigo = tipo.nome
        tipo.nome = novos_dados['nome']
        
        
        db.session.commit()
        return{'message': f"Tipo de flor '{nome_antigo}' atualizado para '{tipo.nome}' com sucesso!"}, 200
    
    
def excluir_tipo(id_tipo):
    tipo = Tipo.query.get(id_tipo)
    if not tipo:
        raise TipoNaoEncontrado(f'Esse tipo de flor não foi encontrado')
    
    nome_tipo = tipo.nome
    db.session.delete(tipo)
    db.session.commit()
    return {'message': f"Tipo de flor '{nome_tipo}'excluído com sucesso!"}, 200