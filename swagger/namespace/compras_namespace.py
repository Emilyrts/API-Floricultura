from flask_restx import Namespace, Resource, fields
from flask import request
from compras.compra_route import criar_compra, listar_compras, obter_compra, atualizar_compra, deletar_compra

api = Namespace('compras', description='Operações relacionadas as compras')

compra_model = api.model('Compra', {
    'data': fields.String(required=True),
    'valor_total': fields.String(required=True),
    'cliente_id': fields.Integer(required=True)
})

@api.route('')
class CompraList(Resource):
    @api.doc('listar_compra')
    def get(self):
        return listar_compras()
    
    @api.expect(compra_model)
    @api.doc('criar_compra')
    def post(self):
        data = request.get_json()
        return criar_compra(data)
    
@api.route('/<int:id_compra>')
@api.param('id_compra', 'ID da compra')
class CompraResource(Resource):
    def get(self, id_compra):
        compra = obter_compra(id_compra)
        if not compra:
            api.abort(404, "Compra não encontrada")
        return compra
    
    def put(self,id_compra):
        compra = atualizar_compra(id_compra, request.get_json())
        if not compra:
            api.abort(404, "Compra não encontrada")
        return compra
    
    def delete(self, id_compra):
        sucesso = deletar_compra(id_compra)
        if not sucesso:
            api.abort(404, "Compra não encontrada")
        return {'message': 'Compra excluída com sucesso.'}
        