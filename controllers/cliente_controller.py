from models.cliente import Cliente  
from flask import Blueprint, request, jsonify
from database import db
from sqlalchemy.exc import IntegrityError

cliente_bp = Blueprint('cliente_bp', __name__)

@cliente_bp.route('/clientes', methods=['POST'])
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

@cliente_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([cliente.to_dict() for cliente in clientes]), 200

@cliente_bp.route('/clientes/<int:id>', methods=['GET'])
def obter_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return jsonify(cliente.to_dict()), 200

@cliente_bp.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    
    nome = request.json.get('nome')
    rg = request.json.get('rg')
    telefone = request.json.get('telefone')
    endereco = request.json.get('endereco')

    # Verifica se o RG existe em outro cliente
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


@cliente_bp.route('/clientes/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return '', 204
