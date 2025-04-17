from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired

class KnowledgeBaseForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    content = TextAreaField('Contenido', validators=[DataRequired()])
    category = StringField('Categoría', validators=[DataRequired()])
    keywords = StringField('Palabras clave')
    is_published = BooleanField('Publicado')
