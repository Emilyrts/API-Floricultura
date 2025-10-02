from flask_restx import Namespace, Resource, fields
from flask import request
from itens.item_route import create_item, get_item, get_all_items, update_item, delete_item

api = Namespace('itens', description='Operações relacionadas aos itens')

item_model = api.model('Item', {
    'compra_id': fields.Integer(required=True),
    'produto_id': fields.Integer(required=True),
    'quantidade': fields.Integer(required=True),
    'valor_unitario': fields.Float(required=True)
})

@api.route('')
class ItemList(Resource):
    @api.doc('get_all_items')
    def get(self):
        return get_all_items()
    
    @api.expect(item_model)
    @api.doc('create_item')
    def post(self):
        data = request.get_json()
        return create_item(data)
    
@api.route('/<id_item>')
@api.param('id_item', 'ID do item')
class ItemResource(Resource):
    def get(self, id_item):
        item = get_item(id_item)
        if not item:
            api.abort(404, "Item não encontrado")
        return item
    
    def put(self, id_item):
        item = update_item(id_item, request.get_json())
        if not item:
            api.abort(404, "Item não encontrado")
        return item
    
    def delete(self, id_item):
        sucesso = delete_item(id_item)
        if not sucesso:
            api.abort(404, "Item não eonctrado")
        return {'message': 'Item deletado com sucesso!'}
        
        