from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from flask_mail import Mail
from authlib.integrations.flask_client import OAuth

# Configuración para SQLAlchemy 2.x
db = SQLAlchemy() #INICIALIZACION DE SQLALCHEMY
migrate = Migrate() #MIGRATE PARA ACTUALIZACION DE BD
login_manager = LoginManager() #LOGIN MANAGER GESTOR DE SESSIONES
mail = Mail() #INICIALIZACION DE MAIL
oauth = OAuth()


#INICIALIZACION/CREACION DE APP 
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializa extensiones

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)  # <-- Añade esta línea
    oauth.init_app(app)
    # Configuración de login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'warning'

    # Define el user_loader para Flask-Login
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Carga el usuario por su ID

    oauth.register(
        name='azure',
        client_id=app.config['AZURE_CLIENT_ID'],
        client_secret=app.config['AZURE_CLIENT_SECRET'],
        access_token_url=f'https://login.microsoftonline.com/{app.config["AZURE_TENANT_ID"]}/oauth2/v2.0/token',
        authorize_url=f'https://login.microsoftonline.com/{app.config["AZURE_TENANT_ID"]}/oauth2/v2.0/authorize',
        api_base_url='https://graph.microsoft.com/v1.0/',
        userinfo_endpoint='https://graph.microsoft.com/oidc/userinfo',
        server_metadata_url=f'https://login.microsoftonline.com/{app.config["AZURE_TENANT_ID"]}/v2.0/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid profile email'}
    )
    # Importa y registra blueprints dentro del contexto
    with app.app_context():
        pass
        #FUNCION CON BLUEPRINTS PARA MEJOR MANEJO DE ROUTES
        from app.routes import (
            auth_routes,
            home_routes,
            ticket_routes,
            asset_ti_routes,
            user_routes,
            knowledge_routes,
            customer_routes,
            cost_center_routes
        )

        app.register_blueprint(auth_routes.bp)
        app.register_blueprint(home_routes.bp)
        app.register_blueprint(ticket_routes.bp)
        app.register_blueprint(asset_ti_routes.bp)
        app.register_blueprint(user_routes.bp)
        app.register_blueprint(knowledge_routes.bp)
        app.register_blueprint(customer_routes.bp)
        app.register_blueprint(cost_center_routes.bp)
    
    return app

