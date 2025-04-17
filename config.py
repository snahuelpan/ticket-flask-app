import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-segura')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
        f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:{os.getenv('DB_PASSWORD', '')}" \
        f"@{os.getenv('DB_HOST', 'localhost')}/{os.getenv('DB_NAME', 'tickets_db')}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }

    # Configuración de correo
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'notificaciones@tusistema.com')
    MAIL_SUBJECT_PREFIX = '[Sistema de Tickets] '

    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
    AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
    AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
    AZURE_REDIRECT_URI = os.getenv("AZURE_REDIRECT_URI")
    AZURE_SCOPES = os.getenv("AZURE_SCOPES")

    # Otros settings comunes
    DEBUG = True
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    # Puedes añadir medidas de seguridad adicionales aquí
    pass

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
