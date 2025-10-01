from typing import List, Optional

from flask import jsonify, request
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel, RootModel
from sqlalchemy.exc import IntegrityError

from config import db

from .cliente_model import Cliente

cliente_tag = Tag(name="clientes", description="Operações relacionadas a clientes")

cliente_bp = APIBlueprint('cliente_routes', __name__, url_prefix='/clientes', abp_tags=[cliente_tag])

class ClienteOut(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str

class ClienteListOut(RootModel[List[ClienteOut]]):
    pass

class MessageResponse(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    message: str
    error: Optional[str] = None

@cliente_bp.post('/', summary='Criar cliente', tags=[cliente_tag], responses={201: ClienteListOut, 404: ErrorResponse})
def criar_cliente():
    nome = request.json.get('nome')
    rg = request.json.get('rg')
    telefone = request.json.get('telefone')
    endereco = request.json.get('endereco')

    novo_cliente = Cliente(nome=nome, rg=rg, telefone=telefone, endereco=endereco)
    db.session.add(novo_cliente)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "RG já cadastrado"}), 400
    return jsonify(novo_cliente.to_dict()), 201

@cliente_bp.get('/', summary='Listar clientes', tags=[cliente_tag], responses={200: ClienteOut, 404: ErrorResponse})
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([cliente.to_dict() for cliente in clientes]), 200

@cliente_bp.get('/<int:id>', summary="Listar cliente por id",tags=[cliente_tag],  responses={201: MessageResponse, 400: ErrorResponse, 500: ErrorResponse})
def obter_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return jsonify(cliente.to_dict()), 200

@cliente_bp.put('/<int:id>', summary="Atualizar cliente",tags=[cliente_tag], responses={200: MessageResponse, 404: ErrorResponse, 500: ErrorResponse})
def atualizar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    
    nome = request.json.get('nome')
    rg = request.json.get('rg')
    telefone = request.json.get('telefone')
    endereco = request.json.get('endereco')

    if rg and Cliente.query.filter(Cliente.rg == rg, Cliente.id != id).first():
        return jsonify({"error": "RG já cadastrado para outro cliente"}), 400


    if nome: cliente.nome = nome
    if rg: cliente.rg = rg
    if telefone: cliente.telefone = telefone
    if endereco: cliente.endereco = endereco

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Erro ao atualizar cliente"}), 500

    return jsonify(cliente.to_dict()), 200


@cliente_bp.delete('/<int:id>', summary="Excluir cliente", tags=[cliente_tag], responses={204: MessageResponse, 404: ErrorResponse, 500: ErrorResponse})
def deletar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return '', 204