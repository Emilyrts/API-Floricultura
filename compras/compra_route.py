from clientes.cliente_model import Cliente
from compras.compra_model import Compra
from flask import Blueprint, request, jsonify
from config import db
from datetime import datetime

compra_bp = Blueprint('compra_routes', __name__, url_prefix='/compras')

@compra_bp.route('/', methods=['POST'])
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

@compra_bp.route('/', methods=['GET'])
def listar_compras():
    compras = Compra.query.all()
    return jsonify([compra.to_dict() for compra in compras]), 200

@compra_bp.route('/<int:id>', methods=['GET'])
def obter_compra(id):
    compra = Compra.query.get_or_404(id)
    return jsonify(compra.to_dict()), 200

from datetime import datetime

@compra_bp.route('/<int:id>', methods=['PUT'])
def atualizar_compra(id):
    compra = Compra.query.get(id)
    
    data_str = request.json.get('data')
    valor_total = request.json.get('valor_total')
    cliente_id = request.json.get('cliente_id')
    
    data = datetime.strptime(data_str, "%Y-%m-%d").date()
    
    compra.data = data
    compra.valor_total = valor_total
    compra.cliente_id = cliente_id
    
    db.session.commit()
    return jsonify(compra.to_dict())    , 200

@compra_bp.route('/<int:id>', methods=['DELETE'])
def deletar_compra(id):
    compra = Compra.query.get_or_404(id)
    db.session.delete(compra)
    db.session.commit()
    return '', 204