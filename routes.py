from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file
from datetime import datetime
from fpdf import FPDF
import pandas as pd

from app import db
from models import Usuario, Cadastro, Beneficio
from werkzeug.security import generate_password_hash

routes = Blueprint('routes', __name__)

def login_obrigatorio(func):
    def wrapper(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Faça login para acessar esta página.', 'error')
            return redirect(url_for('routes.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@routes.route('/')
def home():
    return render_template('index.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = Usuario.query.filter_by(email=request.form['email']).first()
        if usuario and usuario.verificar_senha(request.form['senha']):
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            return redirect(url_for('routes.dashboard'))
        flash('Credenciais inválidas.', 'error')
    return render_template('login.html')

@routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.login'))

@routes.route('/cadastrar_usuario', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])
        usuario = Usuario(nome=nome, email=email, senha_hash=senha)
        db.session.add(usuario)
        db.session.commit()
        flash('Usuário cadastrado com sucesso.', 'success')
        return redirect(url_for('routes.login'))
    return render_template('cadastrar_usuario.html')

@routes.route('/dashboard')
@login_obrigatorio
def dashboard():
    total_tutores = Cadastro.query.count()
    total_beneficios = Beneficio.query.count()
    ranking = db.session.query(Cadastro.nome, db.func.count(Beneficio.id).label('total'))        .join(Beneficio).group_by(Cadastro.id).order_by(db.desc('total')).limit(5).all()
    return render_template('dashboard.html', total_tutores=total_tutores,
                           total_beneficios=total_beneficios, ranking=ranking)

@routes.route('/cadastros')
@login_obrigatorio
def listar_cadastros():
    cadastros = Cadastro.query.all()
    return render_template('cadastros.html', cadastros=cadastros)

@routes.route('/beneficios/<int:cadastro_id>', methods=['GET', 'POST'])
@login_obrigatorio
def beneficios(cadastro_id):
    cadastro = Cadastro.query.get_or_404(cadastro_id)
    tipo_filtro = request.args.get('tipo')
    data_inicio = request.args.get('inicio')
    data_fim = request.args.get('fim')

    beneficios = cadastro.beneficios
    if tipo_filtro:
        beneficios = [b for b in beneficios if b.tipo == tipo_filtro]
    if data_inicio:
        dt_ini = datetime.strptime(data_inicio, '%Y-%m-%d')
        beneficios = [b for b in beneficios if b.data_uso >= dt_ini]
    if data_fim:
        dt_fim = datetime.strptime(data_fim, '%Y-%m-%d')
        beneficios = [b for b in beneficios if b.data_uso <= dt_fim]

    return render_template('beneficios.html', cadastro=cadastro, beneficios=beneficios)

@routes.route('/relatorio/<int:cadastro_id>')
@login_obrigatorio
def gerar_relatorio_pdf(cadastro_id):
    cadastro = Cadastro.query.get_or_404(cadastro_id)
    beneficios = cadastro.beneficios
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Relatório - {cadastro.nome}", ln=1)
    for b in beneficios:
        data = b.data_uso.strftime('%d/%m/%Y %H:%M')
        pdf.cell(200, 10, txt=f"{b.tipo} - {data}", ln=1)
    path = f"/mnt/data/relatorio_{cadastro.id}.pdf"
    pdf.output(path)
    return redirect(f"/download?file=relatorio_{cadastro.id}.pdf")

@routes.route('/relatorio_excel/<int:cadastro_id>')
@login_obrigatorio
def gerar_excel(cadastro_id):
    cadastro = Cadastro.query.get_or_404(cadastro_id)
    beneficios = [{
        'Tipo': b.tipo,
        'Data': b.data_uso.strftime('%d/%m/%Y %H:%M')
    } for b in cadastro.beneficios]
    df = pd.DataFrame(beneficios)
    path = f"/mnt/data/relatorio_{cadastro.id}.xlsx"
    df.to_excel(path, index=False)
    return redirect(f"/download?file=relatorio_{cadastro.id}.xlsx")

@routes.route('/download')
def baixar_arquivo():
    file = request.args.get('file')
    return send_file(f"/mnt/data/{file}", as_attachment=True)
