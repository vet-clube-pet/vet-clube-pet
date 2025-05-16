from app import app, db
from models import UsuarioSistema

with app.app_context():
    admin = UsuarioSistema(
        nome="Raquel Admin",
        email="admin@vetclube.com",
        tipo="admin"
    )
    admin.set_senha("senha123")  # Troque para uma senha forte
    db.session.add(admin)
    db.session.commit()
    print("Administrador criado com sucesso!")
