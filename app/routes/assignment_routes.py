from flask import render_template, request, redirect, url_for, Blueprint
from app import db
from app.models import Assignment, Asset, User, Customer
from datetime import datetime
from app.utils.assignment_forms import AssignmentForm

bp = Blueprint('assignment', __name__, url_prefix='/assignments')

@bp.route('/list', methods=['GET'])
def list():
    """Mostrar lista de asignaciones."""
    assignments = Assignment.query.all()
    return render_template('assignments/list.html', assignments=assignments)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    """Crear nueva asignación."""
    form = AssignmentForm()

    form.asset_id.choices = [(a.id, a.name) for a in Asset.query.all()]
    form.user_id.choices = [(u.id, u.name) for u in User.query.all()]
    form.customer_ids.choices = [(c.id, c.name) for c in Customer.query.all()]

    if form.validate_on_submit():
        assignment = Assignment(
            asset_id=form.asset_id.data,
            user_id=form.user_id.data,
            notes=form.notes.data
        )

        selected_customers = Customer.query.filter(Customer.id.in_(form.customer_ids.data)).all()
        assignment.customers.extend(selected_customers)

        db.session.add(assignment)
        db.session.commit()
        return redirect(url_for('assignments.index'))

    return render_template('assignments/create.html', form=form)

@bp.route('/<int:id>', methods=['GET'])
def assignment_detail(id):
    """Mostrar detalles de una asignación."""
    assignment = Assignment.query.get_or_404(id)
    return render_template('assignments/detail.html', assignment=assignment)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_assignment(id):
    """Editar una asignación."""
    assignment = Assignment.query.get_or_404(id)

    if request.method == 'POST':
        assignment.asset_id = request.form['asset_id']
        assignment.user_id = request.form['user_id']
        assignment.notes = request.form.get('notes')

        db.session.commit()
        return redirect(url_for('assignments.assignment_detail', id=id))

    assets = Asset.query.all()
    users = User.query.all()
    return render_template('assignments/edit.html', assignment=assignment, assets=assets, users=users)
