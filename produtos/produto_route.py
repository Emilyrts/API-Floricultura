from flask import Blueprint, request, jsonify
from produtos.produto_model import ProdutoNaoEncontrado, produto_por_id,listar_produtos, adicionar_produto, atualizar_produto, excluir_produto

produto_bp = Blueprint('produto_routes', __name__, url_prefix='/produtos')

@produto_bp.route('/', methods=['GET'])
def get_produtos():
    return jsonify(listar_produtos())

@produto_bp.route('/<int:id_produto>', methods=['GET'])
def get_produto(id_produto):
    try:
        produto = produto_por_id(id_produto)
        return jsonify(produto)
    
    except ProdutoNaoEncontrado:
        return jsonify({"message": "Produto não encontrado."}), 404
    
@produto_bp.route('/', methods=['POST'])
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
    
@produto_bp.route('/<int:id_produto>', methods=['PUT'])
def put_produto(id_produto):
    try:
        data = request.get_json()
        produto = atualizar_produto(id_produto, data)
        return jsonify({"message": "Produto atualizado com sucesso", "produto": produto})
    
    except ProdutoNaoEncontrado:
        return jsonify({"message": "Produto não encontrado."}), 404
    
@produto_bp.route('/<int:id_produto>', methods=['DELETE'])
def delete_produto(id_produto):
    try:
        excluir_produto(id_produto)
        return jsonify({"message": "Produto deletado com sucesso!"}), 200
    
    except ProdutoNaoEncontrado:
        return jsonify({"message": "Produto não encontado."}), 404
    