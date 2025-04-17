from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Optional
from datetime import datetime, timedelta

class CreateTicketForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[DataRequired()])
    priority = SelectField('Prioridad', choices=[
        ('bajo', 'Bajo'), 
        ('medio', 'Medio'), 
        ('alto', 'Alto'), 
        ('critico', 'Crítico')
    ], default='medio')
    category = SelectField('Categoría', choices=[
        ('hardware', 'Hardware'),
        ('software', 'Software'),
        ('red', 'Red'),
        ('otros', 'Otros')
    ])
    due_date = DateTimeField('Fecha Límite', format='%Y-%m-%d %H:%M', 
                           validators=[Optional()],
                           default=datetime.utcnow() + timedelta(days=3))

class AssignTicketForm(FlaskForm):
    assigned_to = SelectField('Asignar a', coerce=int, validators=[DataRequired()])
    status = SelectField('Estado', choices=[
        ('abierto', 'Abierto'),
        ('en_progreso', 'En Progreso'),
        ('resuelto', 'Resuelto')
    ])

class TicketCommentForm(FlaskForm):
    content = TextAreaField('Comentario', validators=[DataRequired()])
    is_internal = BooleanField('Comentario Interno (no visible para el cliente)')