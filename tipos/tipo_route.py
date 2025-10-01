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

class TipoListOut(RootModel[List[TipoOut]]):
    pass

class MessageResponse(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    message: str
    error: Optional[str] = None

@tipo_bp.get('/', summary='Listar itens', tags=[tipo_tag], responses={200: TipoListOut, 404: ErrorResponse})
def get_tipos():
    return jsonify(listar_tipos()), 200

@tipo_bp.post('/', summary='Criar item', tags=[tipo_tag], responses={201: MessageResponse, 400: ErrorResponse, 500: ErrorResponse})
def post_tipos():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Nome inválido ou ausente"}), 400
        
        novo_tipo = adicionar_tipo(data)
        return jsonify({"message": f"Tipo de flor adicionado com sucesso!"}), 201
    
    except KeyError as e:
        return jsonify({"message": f"Faltando campo obrigatório: {e}"}), 400
    except ValueError as e:
        return jsonify({"message": f"Erro ao processar o nome: {str(e)}"}), 400
