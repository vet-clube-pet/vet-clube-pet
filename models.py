from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    senha_hash = db.Column(db.String(200))

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Cadastro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    pet = db.Column(db.String(100))
    plano = db.Column(db.String(50))
    beneficios = db.relationship('Beneficio', backref='cadastro', lazy=True)

class Beneficio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    data_uso = db.Column(db.DateTime)
    cadastro_id = db.Column(db.Integer, db.ForeignKey('cadastro.id'))
