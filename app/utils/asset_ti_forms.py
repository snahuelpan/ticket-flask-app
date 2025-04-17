from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from app.models import Asset, Software

class AssetForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=120)])
    asset_type = SelectField('Tipo de Asset', choices=[
        ('computadora', 'Computadora'),
        ('monitor', 'Monitor'),
        ('impresora', 'Impresora'),
        ('otro', 'Otro')
    ], validators=[DataRequired()])
    model = StringField('Modelo', validators=[Optional(), Length(max=80)])
    serial_number = StringField('Número de Serie', validators=[DataRequired(), Length(max=80)])
    purchase_date = DateField('Fecha de Compra', validators=[Optional()])
    warranty_expiration = DateField('Fecha de Expiración de Garantía', validators=[Optional()])
    status = SelectField('Estado', choices=[
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('en_mantenimiento', 'En Mantenimiento'),
        ('dado_de_baja', 'Dado de Baja')
    ], default='activo', validators=[DataRequired()])
    location = StringField('Ubicación', validators=[Optional(), Length(max=120)])
    notes = TextAreaField('Notas', validators=[Optional()])

    # Campos adicionales para Software (hereda de Asset)
    license_key = StringField('Clave de Licencia', validators=[Optional(), Length(max=120)])
    license_expiration = DateField('Fecha de Expiración de Licencia', validators=[Optional()])
    version = StringField('Versión', validators=[Optional(), Length(max=50)])

    def validate_serial_number(self, field):
        # Validar que el número de serie sea único en la base de datos
        asset = Asset.query.filter_by(serial_number=field.data).first()
        if asset:
            raise ValidationError('Este número de serie ya está registrado.')
