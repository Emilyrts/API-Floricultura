import os

from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI
from flask_sqlalchemy import SQLAlchemy

info = Info(title="API Floricultura", version="1.0.0", description="Documentação da API Floricultura")

app = OpenAPI(__name__, info=info)
CORS(app)

app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5000
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
