from flask import Flask
from flask_migrate import Migrate
from flasgger import Swagger

from config import app, db
from clientes.cliente_route import cliente_bp
from compras.compra_route import compra_bp
from itens.item_route import item_bp
from produtos.produto_route import produto_bp
from tipos.tipo_route import tipo_bp

app.register_blueprint(cliente_bp)
app.register_blueprint(produto_bp)
app.register_blueprint(compra_bp)
app.register_blueprint(item_bp)
app.register_blueprint(tipo_bp)

@app.route("/", methods=['GET'])
def home():
    return "API Floricultura funcionando!"

migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
