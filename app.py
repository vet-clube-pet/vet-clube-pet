from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'vetclube_secret'

# Banco de dados PostgreSQL via Render ou SQLite local
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///vetclube.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import Usuario, Beneficio
import routes

# Criação automática das tabelas ao iniciar
with app.app_context():
    db.create_all()
