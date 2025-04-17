from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ReturnForm(FlaskForm):
    assignment_id = SelectField('Asignación', coerce=int, validators=[DataRequired()])
    user_id = SelectField('Recibido por', coerce=int, validators=[DataRequired()])
    customer_ids = SelectMultipleField('Cliente(s)', coerce=int, validators=[DataRequired()])
    notes = TextAreaField('Notas')
    submit = SubmitField('Registrar Devolución')
