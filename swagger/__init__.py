from flask_restx import Api
from flask import Blueprint
from swagger.namespace.clientes_namespace import api as clientes_ns
from swagger.namespace.compras_namespace import api as compras_ns
from swagger.namespace.itens_namespace import api as itens_ns
from swagger.namespace.produtos_namespace import api as produtos_ns
from swagger.namespace.tipos_namespace import api as tipos_ns

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/docs', title='Api Floricultura', version='1.0.0', description='Documentação da Api de Floricultura')

api.add_namespace(clientes_ns, path='/clientes')
api.add_namespace(compras_ns, path='/compras')
api.add_namespace(itens_ns, path='/itens')
api.add_namespace(produtos_ns, path='/produtos')
api.add_namespace(tipos_ns, path='/tipos')
