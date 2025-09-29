from typing import List

from flask import jsonify, request
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel, RootModel

from config import db
from produtos.produto_model import Produto

from .item_model import ItemModel

# -----------------------------
# Pydantic Schemas
# -----------------------------

class ErrorResponse(BaseModel):
    message: str
    error: str | None = None
class ItemBase(BaseModel):
    compra_id: int
    produto_id: int
    quantidade: float
class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    quantidade: float
class ItemOut(ItemBase):
    id: int
    valor_unitario: float
    
class ItemListOut(RootModel[List[ItemOut]]):
    pass
class MessageResponse(BaseModel):
    message: str

item_tag = Tag(name="itens", description="Operações relacionadas a itens")
item_bp = APIBlueprint('item_routes', __name__, url_prefix='/itens', abp_tags=[item_tag])

# Rota para criar um novo item (associado a uma compra)
@item_bp.post('/', summary='Criar item', tags=[item_tag], responses={201: ItemOut, 400: ErrorResponse, 404: ErrorResponse, 500: ErrorResponse})
def create_item():
    data = request.get_json()

    # Validação dos dados de entrada
    if not data or 'compra_id' not in data or 'produto_id' not in data or 'quantidade' not in data:
        return jsonify({'message': 'Dados incompletos. É necessário fornecer compra_id, produto_id e quantidade.'}), 400

    # Busca o produto no banco de dados para obter o preço atual
    produto = Produto.query.get(data['produto_id'])

    if not produto:
        return jsonify({'message': 'Produto não encontrado.'}), 404
    
    # Verifica se há estoque suficiente
    if produto.quantidade < data['quantidade']:
        return jsonify({'message': f'Estoque insuficiente para o produto {produto.nome}. Disponível: {produto.quantidade}'}), 400

    # Cria a nova instância do item
    novo_item = ItemModel(
        compra_id=data['compra_id'],
        produto_id=data['produto_id'],
        quantidade=data['quantidade'],
        valor_unitario=produto.preco # Pega o preço diretamente do cadastro do produto
    )

    try:
        # Atualiza o estoque do produto
        produto.quantidade -= data['quantidade']
        db.session.add(produto)
        
        # Salva o novo item
        novo_item.save_to_db()
        
        # NOTE: A lógica de atualização do "valor_total" da COMPRA deve ser tratada
        # preferencialmente na rota de Compra ou via um trigger/callback do modelo.
        
        return jsonify(novo_item.to_json()), 201
    except Exception as e:
        db.session.rollback() # Desfaz as alterações em caso de erro
        return jsonify({'message': 'Ocorreu um erro ao criar o item.', 'error': str(e)}), 500


# Rota para buscar um item específico pelo ID
@item_bp.get('/<int:item_id>',  summary='Listar item por id', tags=[item_tag], responses={200: ItemOut, 404: ErrorResponse})
def get_item(item_id):
    item = ItemModel.find_by_id(item_id)
    if item:
        return jsonify(item.to_json()), 200
    return jsonify({'message': 'Item não encontrado.'}), 404

# Rota para listar todos os itens (pode ser útil para admin, mas use com cuidado)
@item_bp.get('/', summary='Listar itens', tags=[item_tag], responses={200: ItemListOut, 500: ErrorResponse})
def get_all_items():
    itens = ItemModel.query.all()
    return jsonify([item.to_json() for item in itens]), 200

# Rota para atualizar um item (ex: alterar a quantidade)
@item_bp.put('/<int:item_id>', summary='Atualizar item', tags=[item_tag], responses={200: ItemOut, 400: ErrorResponse, 404: ErrorResponse, 500: ErrorResponse})
def update_item(item_id):
    item = ItemModel.find_by_id(item_id)
    if not item:
        return jsonify({'message': 'Item não encontrado.'}), 404

    data = request.get_json()
    nova_quantidade = data.get('quantidade')

    if nova_quantidade is None:
        return jsonify({'message': 'Quantidade não fornecida.'}), 400
    
    try:
        produto = Produto.find_by_id(item.produto_id)
        # Calcula a diferença de quantidade para ajustar o estoque
        diferenca_estoque = item.quantidade - nova_quantidade
        
        if produto.quantidade + diferenca_estoque < 0:
            return jsonify({'message': 'Estoque insuficiente para realizar a alteração.'}), 400
            
        # Ajusta o estoque do produto
        produto.quantidade += diferenca_estoque
        
        # Atualiza a quantidade do item
        item.quantidade = nova_quantidade
        
        # Salva as alterações no banco
        db.session.add(produto)
        item.save_to_db()
        
        return jsonify(item.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Ocorreu um erro ao atualizar o item.', 'error': str(e)}), 500

# Rota para deletar um item
@item_bp.delete('/<int:item_id>',  summary='Excluir item', tags=[item_tag], responses={200: MessageResponse, 404: ErrorResponse, 500: ErrorResponse})
def delete_item(item_id):
    item = ItemModel.find_by_id(item_id)
    if not item:
        return jsonify({'message': 'Item não encontrado.'}), 404

    try:
        # Devolve a quantidade do item ao estoque do produto
        produto = Produto.find_by_id(item.produto_id)
        if produto:
            produto.quantidade += item.quantidade
            db.session.add(produto)
            
        item.delete_from_db()
        
        return jsonify({'message': 'Item deletado com sucesso.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Ocorreu um erro ao deletar o item.', 'error': str(e)}), 500