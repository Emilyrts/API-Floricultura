from flask import Blueprint, request, jsonify
from .cliente_model import Cliente
from config import db
from sqlalchemy.exc import IntegrityError

cliente_bp = Blueprint('cliente_routes', __name__, url_prefix='/clientes')

@cliente_bp.route('/', methods=['POST'])
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
        return {"error": "RG já cadastrado"}, 400
    return [novo_cliente.to_dict()], 201

@cliente_bp.route('/', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return [cliente.to_dict() for cliente in clientes], 200

@cliente_bp.route('/<int:id>', methods=['GET'])
def obter_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return cliente.to_dict(), 200

@cliente_bp.route('/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    
    nome = request.json.get('nome')
    rg = request.json.get('rg')
    telefone = request.json.get('telefone')
    endereco = request.json.get('endereco')

    if rg and Cliente.query.filter(Cliente.rg == rg, Cliente.id != id).first():
        return {"error": "RG já cadastrado para outro cliente"}, 400


    if nome: cliente.nome = nome
    if rg: cliente.rg = rg
    if telefone: cliente.telefone = telefone
    if endereco: cliente.endereco = endereco

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Erro ao atualizar cliente"}, 500

    return cliente.to_dict(), 200


@cliente_bp.route('/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return '', 204