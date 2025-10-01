from typing import List

from flask import jsonify, request
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel, RootModel

from config import db
from produtos.produto_model import Produto

from .item_model import ItemModel

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

@item_bp.post('/', summary='Criar item', tags=[item_tag], responses={201: ItemOut, 400: ErrorResponse, 404: ErrorResponse, 500: ErrorResponse})
def create_item():
    data = request.get_json()

    if not data or 'compra_id' not in data or 'produto_id' not in data or 'quantidade' not in data:
        return jsonify({'message': 'Dados incompletos. É necessário fornecer compra_id, produto_id e quantidade.'}), 400

    produto = Produto.query.get(data['produto_id'])

    if not produto:
        return jsonify({'message': 'Produto não encontrado.'}), 404
    
    if produto.quantidade < data['quantidade']:
        return jsonify({'message': f'Estoque insuficiente para o produto {produto.nome}. Disponível: {produto.quantidade}'}), 400

    novo_item = ItemModel(
        compra_id=data['compra_id'],
        produto_id=data['produto_id'],
        quantidade=data['quantidade'],
        valor_unitario=produto.preco 
    )

    try:

        produto.quantidade -= data['quantidade']
        db.session.add(produto)
        
        novo_item.save_to_db()
        
        return jsonify(novo_item.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Ocorreu um erro ao criar o item.', 'error': str(e)}), 500

@item_bp.get('/<int:item_id>',  summary='Listar item por id', tags=[item_tag], responses={200: ItemOut, 404: ErrorResponse})
def get_item(item_id):
    item = ItemModel.find_by_id(item_id)
    if item:
        return jsonify(item.to_json()), 200
    return jsonify({'message': 'Item não encontrado.'}), 404

@item_bp.get('/', summary='Listar itens', tags=[item_tag], responses={200: ItemListOut, 500: ErrorResponse})
def get_all_items():
    itens = ItemModel.query.all()
    return jsonify([item.to_json() for item in itens]), 200

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
        diferenca_estoque = item.quantidade - nova_quantidade
        
        if produto.quantidade + diferenca_estoque < 0:
            return jsonify({'message': 'Estoque insuficiente para realizar a alteração.'}), 400
       
        produto.quantidade += diferenca_estoque
       
        item.quantidade = nova_quantidade
        
        db.session.add(produto)
        item.save_to_db()
        
        return jsonify(item.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Ocorreu um erro ao atualizar o item.', 'error': str(e)}), 500

@item_bp.delete('/<int:item_id>',  summary='Excluir item', tags=[item_tag], responses={200: MessageResponse, 404: ErrorResponse, 500: ErrorResponse})
def delete_item(item_id):
    item = ItemModel.find_by_id(item_id)
    if not item:
        return jsonify({'message': 'Item não encontrado.'}), 404

    try:
        produto = Produto.find_by_id(item.produto_id)
        if produto:
            produto.quantidade += item.quantidade
            db.session.add(produto)
            
        item.delete_from_db()
        
        return jsonify({'message': 'Item deletado com sucesso.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Ocorreu um erro ao deletar o item.', 'error': str(e)}), 500