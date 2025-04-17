from flask import Blueprint, render_template, redirect, url_for, flash, request , session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from app.models import User
from app.utils.forms import LoginForm, RegistrationForm
from app import db, oauth
from authlib.common.security import generate_token
import uuid

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    print(current_user)

    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            #flash('Has iniciado sesión correctamente.', 'success')
            return redirect(next_page or url_for('home.index'))
        flash('Email o contraseña incorrectos.', 'danger')
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            name=form.name.data,
            lastname=form.lastname.data,
            uuid=str(uuid.uuid4()) # Necesitarás implementar esta función
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('¡Tu cuenta ha sido creada! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    # TODO: Implementar lógica de recuperación de contraseña
    return render_template('auth/reset_password.html')


@bp.route('/login-azure')
def login_azure():
    nonce = generate_token()  # genera un token aleatorio
    session['nonce'] = nonce  # guárdalo en sesión
    redirect_uri = url_for('auth.callback', _external=True)
    return oauth.azure.authorize_redirect(redirect_uri, nonce=nonce)


@bp.route('/callback')
def callback():
    token = oauth.azure.authorize_access_token()
    user_info = oauth.azure.parse_id_token(token, nonce=session.get('nonce'))

    # Buscar o crear usuario
    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        #user = User(name=user_info['name'], email=user_info['email'])
        #db.session.add(user)
        #db.session.commit()
        logout_user()
        flash('Cuenta no Habilitada', 'danger')
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('home.index'))