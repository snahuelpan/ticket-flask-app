import uuid
import click
import os
from flask import Flask
from app import create_app, db
from app.models import User
from config import Config, ProductionConfig
from werkzeug.security import generate_password_hash


config_type = os.getenv('APP_ENV', 'development')

if config_type == 'production':
    app = create_app(ProductionConfig)
else:
    app = create_app(Config)

@app.cli.command('resetdb')
@click.confirmation_option(prompt='¿Estás seguro de que quieres recrear la base de datos?')
def initdb_command():
    """Inicializa la base de datos."""
    print(db)
    #db.drop_all()
    #db.create_all()
    # Crear un usuario de prueba
    test_user = User(
        email='soporteti@local.com',
        password_hash=generate_password_hash('ADMIN'), ##CAMBIAR CONTRASEÑA
        name="Departamento",
        lastname="Informatica",
        uuid=str(uuid.uuid4())
    )
    
    # Agregar el usuario de prueba a la base de datos
    db.session.add(test_user)
    db.session.commit()

    print('Base de datos inicializada exitosamente.')
    print(f'Usuario de prueba creado: {test_user.email}')

if __name__ == '__main__':
    #initdb_command()
    app.run(port=3000)