from flask_restx import Resource, Namespace, fields
from flask import request
from clientes.cliente_route import criar_cliente, listar_clientes, obter_cliente, atualizar_cliente, deletar_cliente

api = Namespace('clientes', description='Operações relacionadas aos alunos')

cliente_model= api.model('Clientes', {
    'nome': fields.String(required=True),
    'rg': fields.String(required=True),
    'telefone': fields.String(required=True),
    'endereco': fields.String(required=True)
})

@api.route('')
class ClienteList(Resource):
    @api.doc('listar_clientes')
    def get(self):
        return listar_clientes()
    
    @api.expect(cliente_model)
    @api.doc('criar_cliente')
    def post(self):
        data = request.get_json()
        return criar_cliente(data)
    
@api.route('/<int:id_cliente>')
@api.param('id_cliente', 'ID do Cliente')
class ClienteResource(Resource):
    def get(self, id_cliente):
        cliente = obter_cliente(id_cliente)
        if not cliente:
            api.abort(404, "Cliente não encontrado")
        return cliente
    
    def put(self, id_cliente):
        cliente = atualizar_cliente(id_cliente, request.get_json())
        if not cliente:
            api.abort(404, "Cliente não encontrado")
        return cliente
    
    def delete(self, id_cliente):
        sucesso = deletar_cliente(id_cliente)
        if not sucesso:
            api.abort(404, "Cliente não encontrado")
        return {'message': "Cliente excluído com sucesso"}
    
    