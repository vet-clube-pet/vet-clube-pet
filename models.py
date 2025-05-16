from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# Modelo principal: tutor com plano
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    plano = db.Column(db.String(20), nullable=False)
    consultas_usadas = db.Column(db.Integer, default=0)
    exames_usados = db.Column(db.Integer, default=0)
    procedimentos_usados = db.Column(db.Integer, default=0)

# Modelo de controle de benefícios por tutor
class Beneficio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # exemplo: consulta, exame
    usado_em = db.Column(db.DateTime, nullable=False)

# Modelo para login no sistema
class UsuarioSistema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # admin ou funcionario

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
