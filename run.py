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
    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    app.run(port=3000)