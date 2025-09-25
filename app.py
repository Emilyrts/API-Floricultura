import os
from flask import Flask
from config import Config
from database import db
from controllers.cliente_controller import cliente_bp
from controllers.compra_controller import compra_bp  

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# registrar os blueprints
app.register_blueprint(cliente_bp)
app.register_blueprint(compra_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
