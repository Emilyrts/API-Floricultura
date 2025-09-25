from flask import Blueprint, request, jsonify
from .tipo_model import TipoNaoEncontrado, listar_tipos, adicionar_tipo, atualizar_tipo, excluir_tipo

tipos_blueprint = Blueprint('tipos', __name__)

@tipos_blueprint.route('/tipos', methods=['GET'])
def get_tipos():
    return jsonify(listar_tipos()), 200

@tipos_blueprint.route('/tipos', methods=['POST'])
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
    
@tipos_blueprint.route('/tipos/<int:id_tipo>', methods=['PUT'])
def put_tipo(id_tipo):
    try:
        data = request.get_json()
        tipo = atualizar_tipo(id_tipo, data)
        return jsonify ({"message": "Tipo atualizado com sucesso", "tipo":tipo})
    
    except TipoNaoEncontrado:
        return jsonify({"message": "Tipo de flor não encontrado"}), 404
    
@tipos_blueprint.route('/tipos/<int:id_tipo>', methods=['DELETE'])
def delete_aluno(id_tipo):
    try:
        excluir_tipo(id_tipo)
        return jsonify({"message": "Tipo de flor deletado com sucesso!"}), 200
    
    except TipoNaoEncontrado:
        return jsonify({"message": "Tipo de flor não encontrado"}), 404

