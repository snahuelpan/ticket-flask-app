from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email

class CostCenterForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    branch = StringField('Sucursal', validators=[DataRequired()])
    location = StringField('Faena', validators=[DataRequired()])
    id_number = StringField('N° Centro Costo', validators=[DataRequired()])
    management = StringField('Gerencia', validators=[DataRequired()])
    manager = StringField('Gerente', validators=[DataRequired()])
    email_manager = StringField('Mail Gerente', validators=[DataRequired(), Email()])
    administrator = StringField('Nombre Administrador', validators=[DataRequired()])
    administrator_email = StringField('Mail Administrador', validators=[DataRequired(), Email()])
    administrator_cellphone = StringField('N° Celular administrador', validators=[DataRequired()])
