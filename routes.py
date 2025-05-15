
from flask import render_template, request, redirect, url_for
from app import app, db
from models import Usuario, Beneficio

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        plano = request.form["plano"]
        novo_usuario = Usuario(nome=nome, telefone=telefone, email=email, plano=plano)
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for("sucesso"))
    return render_template("cadastro.html")

@app.route("/sucesso")
def sucesso():
    return render_template("sucesso.html")
