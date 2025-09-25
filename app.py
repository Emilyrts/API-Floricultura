from config import app, db
from tipo.tipo_route import tipos_blueprint
from produtos.produto_route import produtos_bp
from clientes.cliente_route import cliente_bp
from compras.compra_route import compra_bp

app.register_blueprint(tipos_blueprint)
app.register_blueprint(produtos_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(compra_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(
        host = app.config['HOST'],
        port = app.config['PORT'],
        debug = app.config['DEBUG']
    )