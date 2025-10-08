from flask_restx import Namespace, Resource, fields
from flask import request
from tipos.tipo_model import TipoNaoEncontrado, listar_tipos, adicionar_tipo, atualizar_tipo, excluir_tipo, tipo_por_id

api = Namespace ('tipos', description='Operações relacionadas aos tipos de produtos')

tipo_model= api.model('Tipo', {
    'nome': fields.String(required=True)
})

@api.route('')
class TipoList(Resource):
    @api.doc('listar_tipos')
    def get(self):
        return listar_tipos()
    
    @api.expect(tipo_model)
    @api.doc('adicionar_tipo')
    def post(self):
        data = request.get_json()
        return adicionar_tipo(data)
    
@api.route('/<int:id_tipo>')
@api.param('id_tipo', 'ID do tipo')
class TipoResource(Resource):
    def get(self, id_tipo):
        try:
            return tipo_por_id(id_tipo)
        except TipoNaoEncontrado:
            api.abort(404, "Tipo de produto não encontrado")
            
    @api.expect(tipo_model)
    def put(self, id_tipo):
        try:
            return atualizar_tipo(id_tipo, request.get_json())
        except TipoNaoEncontrado:
            api.abort(404, 'Tipo de produto não encontrado')
            
    def delete(self, id_tipo):
        try:
            excluir_tipo(id_tipo)
            return {'message': 'Tipo de produto excluído com sucesso!'}
        except TipoNaoEncontrado:
            api.abort(404, 'Tipo de produto não encontrado')
