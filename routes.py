
from flask import render_template, request, redirect, url_for, session
from app import app, db
from models import Usuario, Beneficio, UsuarioSistema

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
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    usuarios = Usuario.query.all()
    return render_template('cadastros.html', usuarios=usuarios)

@app.route('/beneficios/<int:usuario_id>')
def beneficios(usuario_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    usuario = Usuario.query.get_or_404(usuario_id)
    return render_template('beneficios.html', usuario=usuario)

@app.route('/cadastrar_usuario')
def cadastrar_usuario():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    return render_template('cadastrar_usuario.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = UsuarioSistema.query.filter_by(email=email).first()

        if usuario and usuario.verificar_senha(senha):
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            session['usuario_tipo'] = usuario.tipo
            return redirect(url_for('cadastros'))
        else:
            erro = 'E-mail ou senha inválidos.'

    return render_template('login.html', erro=erro)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
