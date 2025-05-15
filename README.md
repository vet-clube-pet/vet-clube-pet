# Vet Clube Pet (versão online)

Sistema web para gerenciamento de tutores, pets, planos e benefícios com login, painel administrativo, exportação e filtros.

## 🚀 Deploy automático no Render

1. Suba este projeto no GitHub
2. Crie um novo Web Service em https://render.com
3. Preencha:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
   - Runtime: Python
4. Crie uma instância PostgreSQL no Render e copie o DATABASE_URL
5. Adicione as variáveis de ambiente:
   - FLASK_ENV = production
   - SECRET_KEY = vetclube_secret
   - DATABASE_URL = <valor do PostgreSQL>

## 👤 Login padrão

- Email: `admin@vet.com`
- Senha: `senha123`

## 📁 Estrutura do projeto

- `app.py` → inicia o Flask
- `models.py` → modelos SQLAlchemy
- `routes.py` → rotas e lógica
- `templates/` → páginas HTML
- `static/` → arquivos CSS/JS
