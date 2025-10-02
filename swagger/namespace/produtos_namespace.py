from flask_restx import Namespace, Resource, fields
from flask import request
from produtos.produto_model import ProdutoNaoEncontrado, produto_por_id, listar_produtos, adicionar_produto, atualizar_produto, excluir_produto

api = Namespace('produtos', description = 'Opreações relacionadas aos produtos')

produto_model = api.model('Produto',  {
    'nome': fields.String(required=True),
    'quantidade': fields.Integer(required=True),
    'preco': fields.Float(required=True),
    'tipo_id': fields.Integer(required=True)
})


@api.route('')
class ProdutoList(Resource):
    @api.doc('listar_produtos')
    def get(self):
        return listar_produtos()
    
    @api.expect(produto_model)
    @api.doc('adicionar_produto')
    def post(self):
        data = request.get_json()
        return adicionar_produto(data)
    
@api.route('/<int:id_produto>')
@api.param('id_produto', 'ID do produto')
class ProdutoResource(Resource):
    def get(self, id_produto):
        try:
            return produto_por_id(id_produto)
        except ProdutoNaoEncontrado:
            api.abort(404, "Produto não encontrado")
            
    @api.expect(produto_model)
    def put(self, id_produto):
        try:
            return atualizar_produto(id_produto, request.get_json())
        except ProdutoNaoEncontrado:
            api.abort(404, "Produto não encontrado")
            
    def delete(self, id_produto):
        try:
            excluir_produto(id_produto)
            return {'message': 'Produto excluído com sucesso'}
        except ProdutoNaoEncontrado:
            api.abort(404, "Produto não encontrado")
        