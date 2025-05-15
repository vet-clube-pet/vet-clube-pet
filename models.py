
from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    plano = db.Column(db.String(50))
    consultas_usadas = db.Column(db.Integer, default=0)
    exames_usados = db.Column(db.Integer, default=0)
    procedimentos_usados = db.Column(db.Integer, default=0)

class Beneficio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    tipo = db.Column(db.String(50))
    quantidade = db.Column(db.Integer)
