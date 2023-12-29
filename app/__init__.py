from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'a89hn7AKJYAVTSdtuvyias6vuaysD&IViajkvsd6i8vaDUJr'
jwt = JWTManager(app)
from app import routes