from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import User
from app.utils.users_forms import UserForm
import uuid

bp = Blueprint('users', __name__, url_prefix='/users')

# Ruta para listar todos los usuarios
@bp.route('/list')
@login_required
def list_users():
    users = User.query.all()  # Obtener todos los usuarios
    return render_template('users/list.html', users=users)

# Ruta para ver los detalles de un usuario
@bp.route('/<int:user_id>/details')
@login_required
def user_details(user_id):
    user = User.query.get_or_404(user_id)  # Obtener el usuario por su ID
    return render_template('users/details.html', user=user)

# Ruta para crear un nuevo usuario
@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_user():
    form = UserForm()

    if form.validate_on_submit():
        # Crear un nuevo usuario
        
        user = User(
            uuid=str(uuid.uuid4()),
            name=form.name.data,
            lastname=form.lastname.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Usuario creado exitosamente!', 'success')
        return redirect(url_for('users.list_users'))

    return render_template('users/create.html', form=form)

# Ruta para editar un usuario
@bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)

    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.password = form.password.data  # Asegúrate de hashear la contraseña
        db.session.commit()
        flash('Usuario actualizado exitosamente!', 'success')
        return redirect(url_for('users.list_users'))

    return render_template('users/edit.html', form=form, user=user)

# Ruta para eliminar un usuario
@bp.route('/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado exitosamente!', 'danger')
    return redirect(url_for('users.list_users'))
