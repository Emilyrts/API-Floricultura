from typing import List, Optional

from flask import jsonify, request
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel, RootModel

from config import db
from produtos.produto_model import (ProdutoNaoEncontrado, adicionar_produto,
                                    atualizar_produto, excluir_produto,
                                    listar_produtos, produto_por_id)

produto_tag = Tag(name="produtos", description="Operações relacionadas a produtos")
produto_bp = APIBlueprint('produtos_routes', __name__, url_prefix='/produtos', abp_tags=[produto_tag])

class ProdutoOut(BaseModel):
    id: int
    nome: str
    quantidade: float
    preco: float
    tipo_id: int

# Para lista de produtos (RootModel para Pydantic v2)
class ProdutoListOut(RootModel[List[ProdutoOut]]):
    pass

# Mensagem de sucesso genérica
class MessageResponse(BaseModel):
    message: str

# Mensagem de erro padrão
class ErrorResponse(BaseModel):
    message: str
    error: Optional[str] = None

@produto_bp.get('/', summary='Listar produtos', tags=[produto_tag], responses={200: ProdutoOut, 500: ErrorResponse})
def get_produtos():
    return jsonify(listar_produtos())

@produto_bp.get('/<int:id_produto>', summary='Listar produto por id', tags=[produto_tag], responses={200: ProdutoOut, 404: ErrorResponse})
def get_produto(id_produto):
    try:
        produto = produto_por_id(id_produto)
        return jsonify(produto)
    
    except ProdutoNaoEncontrado:
        return jsonify({"message": "Produto não encontrado."}), 404
    
@produto_bp.post('/', summary='Criar produto por id', tags=[produto_tag], responses={201: MessageResponse, 404: ErrorResponse, 500: ErrorResponse})
def post_produto():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Dados inválidos ou ausentes"}), 400
        novo_produto = adicionar_produto(data)
        return jsonify({"message": "Produto adicionado com sucesso"}), 201
    
    except KeyError as e:
        return jsonify({"message": f"Faltando campo obrigatório: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"message": f"Erro ao processar os dados: {str(e)}"}), 400
    
@produto_bp.put('/<int:id_produto>', summary='Atulizar produto', tags=[produto_tag], responses={200: MessageResponse, 404: ErrorResponse, 500: ErrorResponse})
def put_produto(id_produto):
    try:
        data = request.get_json()
        produto = atualizar_produto(id_produto, data)
        return jsonify({"message": "Produto atualizado com sucesso", "produto": produto})
    
    except ProdutoNaoEncontrado:
        return jsonify({"message": "Produto não encontrado."}), 404
    
@produto_bp.delete('/<int:id_produto>', summary='Excluir produto', tags=[produto_tag], responses={200: MessageResponse, 404: ErrorResponse, 500: ErrorResponse})
def delete_produto(id_produto):
    try:
        excluir_produto(id_produto)
        return jsonify({"message": "Produto deletado com sucesso!"}), 200
    
    except ProdutoNaoEncontrado:
        return jsonify({"message": "Produto não encontado."}), 404
    