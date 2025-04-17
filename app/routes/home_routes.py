from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Ticket, TicketComment
from app import db

# Crea el Blueprint con nombre y prefijo de URL
bp = Blueprint('home', __name__,url_prefix='/home')

@bp.route('/')
@login_required
def index():
    active_tickets_count = Ticket.query.filter_by(requester_id=current_user.id, status='abierto').count()
    return render_template('home/index.html', active_tickets_count=active_tickets_count)