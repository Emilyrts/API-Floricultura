from flask_migrate import Migrate

from clientes.cliente_route import cliente_bp
from compras.compra_route import compra_bp
from config import app, db
from itens.item_route import item_bp
from produtos.produto_route import produto_bp
from tipos.tipo_route import tipo_bp

# registrar APIBlueprints (não Blueprints comuns)
app.register_api(tipo_bp)
app.register_api(produto_bp)
app.register_api(cliente_bp)
app.register_api(compra_bp)
app.register_api(item_bp)

@app.get("/")
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
