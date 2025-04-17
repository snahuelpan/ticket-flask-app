from flask import render_template, current_app
from flask_mail import Message
from app import mail
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(
        subject=current_app.config['MAIL_SUBJECT_PREFIX'] + subject,
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=recipients
    )
    msg.html = render_template(f'emails/{template}.html', **kwargs)
    
    # Envío asíncrono
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

def notify_ticket_created(ticket):
    send_email(
        f"Nuevo Ticket #{ticket.id}: {ticket.title}",
        [ticket.requester_id.email],
        'ticket_created',
        ticket=ticket
    )

def notify_ticket_assigned(ticket, previous_assignee=None):
    recipients = [ticket.assigned_to.email]
    if previous_assignee and previous_assignee != ticket.assigned_to:
        recipients.append(previous_assignee.email)
    
    send_email(
        f"Ticket #{ticket.id} asignado a ti",
        recipients,
        'ticket_assigned',
        ticket=ticket
    )

def notify_ticket_comment(ticket, comment):
    recipients = {ticket.requester.email, ticket.assigned_to.email} - {comment.user.email}
    if recipients:
        send_email(
            f"Nuevo comentario en Ticket #{ticket.id}",
            list(recipients),
            'ticket_comment',
            ticket=ticket,
            comment=comment
        )