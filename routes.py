from flask import render_template, request, redirect, url_for
from app import app, db
from models import Usuario, Beneficio

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        plano = request.form['plano']

        usuario = Usuario(
            nome=nome,
            telefone=telefone,
            email=email,
            plano=plano,
            consultas_usadas=0,
            exames_usados=0,
            procedimentos_usados=0
        )
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('sucesso'))

    return render_template('cadastro.html')

@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')

@app.route('/cadastros')
def cadastros():
    usuarios = Usuario.query.all()
    return render_template('cadastros.html', usuarios=usuarios)

@app.route('/beneficios/<int:usuario_id>')
def beneficios(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    return render_template('beneficios.html', usuario=usuario)

@app.route('/cadastrar_usuario')
def cadastrar_usuario():
    return render_template('cadastrar_usuario.html')

# ✅ ROTA TEMPORÁRIA PARA CRIAR TABELAS
@app.route('/criar-tabelas')
def criar_tabelas():
    db.create_all()
    return "Tabelas criadas com sucesso!"
