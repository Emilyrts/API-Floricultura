from typing import List, Optional

from flask import jsonify, request
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel, RootModel

from config import db

from .tipo_model import (TipoNaoEncontrado, adicionar_tipo, atualizar_tipo,
                         excluir_tipo, listar_tipos)

tipo_tag = Tag(name="tipos", description="Operações relacionadas a tipos")
tipo_bp = APIBlueprint('tipo_routes', __name__, url_prefix='/tipos', abp_tags=[tipo_tag])

class TipoOut(BaseModel):
    id: int
    nome: str

# Para lista de tipos (RootModel para Pydantic v2)
class TipoListOut(RootModel[List[TipoOut]]):
    pass

# Mensagem de sucesso genérica
class MessageResponse(BaseModel):
    message: str

# Mensagem de erro padrão
class ErrorResponse(BaseModel):
    message: str
    error: Optional[str] = None

@tipo_bp.get('/tipos', summary='Listar itens', tags=[tipo_tag], responses={200: TipoListOut, 404: ErrorResponse})
def get_tipos():
    return jsonify(listar_tipos()), 200

@tipo_bp.post('/tipos', summary='Criar item', tags=[tipo_tag], responses={201: MessageResponse, 400: ErrorResponse, 500: ErrorResponse})
def post_tippos():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message":"Nome invélido ou ausente"}), 400
        
        novo_tipo = adicionar_tipo(data)
        return jsonify({"message": f"Tipo de flor adicionado com sucesso!"}), 201
    
    except KeyError as e:
        return jsonify({"message": f"Faltando campo obrigatório: {(e)}"}), 400
    
    except ValueError as e:
        return jsonify({"message": f"Erro aos processar o nome: {str(e)}"}), 400
    
@tipo_bp.put('/<int:id_tipo>', summary='Atualizar item', tags=[tipo_tag], responses={200: MessageResponse, 404: ErrorResponse, 500: ErrorResponse})
def put_tipo(id_tipo):
    try:
        data = request.get_json()
        tipo = atualizar_tipo(id_tipo, data)
        return jsonify ({"message": "Tipo atualizado com sucesso", "tipo":tipo})
    
    except TipoNaoEncontrado:
        return jsonify({"message": "Tipo de flor não encontrado"}), 404
    
@tipo_bp.delete('/<int:id_tipo>', summary='Excluir item', tags=[tipo_tag], responses={200: MessageResponse, 404: ErrorResponse, 500: ErrorResponse})
def delete_aluno(id_tipo):
    try:
        excluir_tipo(id_tipo)
        return jsonify({"message": "Tipo de flor deletado com sucesso!"}), 200
    
    except TipoNaoEncontrado:
        return jsonify({"message": "Tipo de flor não encontrado"}), 404
