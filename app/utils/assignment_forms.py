from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class AssignmentForm(FlaskForm):
    asset_id = SelectField('Activo', coerce=int, validators=[DataRequired()])
    user_id = SelectField('Entregado por', coerce=int, validators=[DataRequired()])
    customer_ids = SelectMultipleField('Clientes', coerce=int, validators=[DataRequired()])
    notes = TextAreaField('Notas')
    submit = SubmitField('Asignar')
