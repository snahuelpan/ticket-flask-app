from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Ticket, TicketComment, User
from app.utils.ticket_forms import CreateTicketForm, AssignTicketForm, TicketCommentForm
from app.services.notification_service import (
    notify_ticket_created,
    notify_ticket_assigned,
    notify_ticket_comment
)

bp = Blueprint('ticket', __name__, url_prefix='/tickets')

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateTicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            category=form.category.data,
            due_date=form.due_date.data,
            requester_id=current_user.id
        )
        db.session.add(ticket)
        db.session.commit()
        #notify_ticket_created(ticket)  # <-- en desarrollo
        flash('Ticket creado exitosamente!', 'success')
        return redirect(url_for('ticket.detail', ticket_id=ticket.id))
    return render_template('tickets/create.html', form=form)

@bp.route('/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    comment_form = TicketCommentForm()
    assign_form = AssignTicketForm()
    
    # Cargar opciones para asignación
    assign_form.assigned_to.choices = [(u.id, f"{u.name} {u.lastname}") 
                                     for u in User.query.filter(User.id != current_user.id).all()]
    
    if comment_form.validate_on_submit():
        comment = TicketComment(
            content=comment_form.content.data,
            is_internal=comment_form.is_internal.data,
            user_id=current_user.id,
            ticket_id=ticket.id
        )
        db.session.add(comment)
        db.session.commit()
        notify_ticket_comment(ticket, comment)  # <-- Añade esta línea
        flash('Comentario añadido', 'success')
        return redirect(url_for('ticket.detail', ticket_id=ticket.id))
    
    if assign_form.validate_on_submit():
        previous_assignee = ticket.assigned_to
        ticket.assigned_to_id = assign_form.assigned_to.data
        ticket.status = assign_form.status.data
        db.session.commit()
        notify_ticket_assigned(ticket, previous_assignee)  # <-- Añade esta línea
        flash('Ticket asignado exitosamente', 'success')
        return redirect(url_for('ticket.detail', ticket_id=ticket.id))
    
    return render_template('tickets/details.html', 
                         ticket=ticket, 
                         comment_form=comment_form,
                         assign_form=assign_form)

@bp.route('/list')
@login_required
def list():
    # Filtros básicos
    status_filter = request.args.get('status', 'all')
    query = Ticket.query
    
    if status_filter == 'open':
        query = query.filter(Ticket.status.in_(['abierto', 'en_progreso']))
    elif status_filter == 'my_tickets':
        query = query.filter(Ticket.assigned_to_id == current_user.id)
    elif status_filter == 'created_by_me':
        query = query.filter(Ticket.requester_id == current_user.id)
    
    tickets = query.order_by(Ticket.due_date.asc()).all()
    return render_template('tickets/list.html', tickets=tickets, status_filter=status_filter)