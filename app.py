import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'vetclube_secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'os.getenv('DATABASE_URL', 'sqlite:///vetclube.db')'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from routes import routes
    app.register_blueprint(routes)

    with app.app_context():
        from models import Usuario
        db.create_all()
        if not Usuario.query.filter_by(email='admin@vet.com').first():
            from werkzeug.security import generate_password_hash
            admin = Usuario(nome='Admin', email='admin@vet.com', senha_hash=generate_password_hash('senha123'))
            db.session.add(admin)
            db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
