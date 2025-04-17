from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Optional
from datetime import datetime, timedelta

class CreateTicketForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    customer = SelectField('Trabajador', validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[DataRequired()])
    priority = SelectField('Prioridad', choices=[
        ('bajo', 'Bajo'), 
        ('medio', 'Medio'), 
        ('alto', 'Alto'), 
        ('critico', 'Crítico')
    ], default='medio')
    category = SelectField('Categoría', choices=[
        ("correo corporativo" , "Correo corporativo"), 
        ("preparacion de equipo" , "Preparacion de equipo"),
        ("instalacion de programas" , "Instalacion de programas"),
        ("problemas de conexión" , "problemas de conexión"),
        ("problemas de office 365" , "problemas de office 365"),
        #sharepoint / onedrive
        ("configuracion de Software" , "Configuracion de Software"),
        #Configuracion Equipo
        #Configuracion Correo
        #Problemas de Aplicaciones
        #compra de equipo
        #instalacion de impresora
        #Problemas con impresora
        #Bloqueo de correo
        #Reparacion de Equipo
        #Firma de Correo
        #Creacion de pie de firma
        #Cambio de equipo
        #Visita en Terreno
        #Devolucion de equipo
        #Kit Informatico
        #Cotización de equipos
        ("problema con computador" ,"Problema con computador"),
        ("otro" , "Otro")
     
    ], default='Red')
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