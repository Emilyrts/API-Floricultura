from datetime import datetime
from typing import List, Optional

from flask import jsonify, request
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel, RootModel

from clientes.cliente_model import Cliente
from compras.compra_model import Compra
from config import db

compra_tag = Tag(name="compras",description="Operações relacionadas a compras")
compra_bp = APIBlueprint("compra_routes", __name__, url_prefix="/compras",abp_tags=[compra_tag])

class CompraOut(BaseModel):
    id: int
    data: datetime
    valor_total: float
    cliente_id: int

# Lista de compras
class CompraListOut(RootModel[List[CompraOut]]):
    pass

# Mensagem de sucesso genérica
class MessageResponse(BaseModel):
    message: str

# Mensagem de erro padrão
class ErrorResponse(BaseModel):
    message: str
    error: Optional[str] = None

@compra_bp.post('/', summary="Criar compra",tags=[compra_tag], responses={201: MessageResponse, 400: ErrorResponse, 500: ErrorResponse})
def criar_compra():
    data_str = request.json.get('data')  # string "YYYY-MM-DD"
    valor_total = request.json.get('valor_total')
    cliente_id = request.json.get('cliente_id')

    # converte para datetime.date
    data = datetime.strptime(data_str, "%Y-%m-%d").date()

    nova_compra = Compra(data=data, valor_total=valor_total, cliente_id=cliente_id)
    db.session.add(nova_compra)
    db.session.commit()
    return jsonify(nova_compra.to_dict()), 201

@compra_bp.get('/', responses={200: CompraListOut, 404: ErrorResponse})
def listar_compras():
    compras = Compra.query.all()
    return jsonify([compra.to_dict() for compra in compras]), 200

@compra_bp.get('/<int:id>', summary="Listar compra por id",tags=[compra_tag], responses={200: CompraOut, 404: ErrorResponse})
def obter_compra(id):
    compra = Compra.query.get_or_404(id)
    return jsonify(compra.to_dict()), 200

from datetime import datetime


@compra_bp.put('/<int:id>', summary="Atualizar compra",tags=[compra_tag], responses={200: MessageResponse, 404: ErrorResponse, 500: ErrorResponse})
def atualizar_compra(id):
    compra = Compra.query.get(id)
    
    data_str = request.json.get('data')
    valor_total = request.json.get('valor_total')
    cliente_id = request.json.get('cliente_id')
    
    # converter string para datetime.date
    data = datetime.strptime(data_str, "%Y-%m-%d").date()
    
    compra.data = data
    compra.valor_total = valor_total
    compra.cliente_id = cliente_id
    
    db.session.commit()
    return jsonify(compra.to_dict()), 200


@compra_bp.delete('/<int:id>', summary="Excluir compra",tags=[compra_tag], responses={200: MessageResponse, 404: ErrorResponse, 500: ErrorResponse})
def deletar_compra(id):
    compra = Compra.query.get_or_404(id)
    db.session.delete(compra)
    db.session.commit()
    return '', 204