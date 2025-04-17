from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import KnowledgeBaseArticle
from app.utils.knowledge_base_forms import KnowledgeBaseForm

bp = Blueprint('knowledge_base', __name__, url_prefix='/knowledge_base')

# Ruta para listar todos los artículos
@bp.route('/list')
@login_required
def list_articles():
    articles = KnowledgeBaseArticle.query.all()  # Obtener todos los artículos
    return render_template('knowledge_base/list.html', articles=articles)

# Ruta para ver los detalles de un artículo
@bp.route('/<int:article_id>/details')
@login_required
def article_details(article_id):
    article = KnowledgeBaseArticle.query.get_or_404(article_id)  # Obtener el artículo por su ID
    article.views += 1  # Incrementar vistas
    db.session.commit()
    return render_template('knowledge_base/details.html', article=article)

# Ruta para crear un nuevo artículo
@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_article():
    form = KnowledgeBaseForm()

    if form.validate_on_submit():
        # Crear un nuevo artículo
        article = KnowledgeBaseArticle(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            keywords=form.keywords.data,
            author_id=current_user.id  # Relacionar con el usuario actual
        )
        db.session.add(article)
        db.session.commit()
        flash('Artículo creado exitosamente!', 'success')
        return redirect(url_for('knowledge_base.list_articles'))

    return render_template('knowledge_base/create.html', form=form)

# Ruta para editar un artículo
@bp.route('/<int:article_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = KnowledgeBaseArticle.query.get_or_404(article_id)
    form = KnowledgeBaseForm(obj=article)

    if form.validate_on_submit():
        article.title = form.title.data
        article.content = form.content.data
        article.category = form.category.data
        article.keywords = form.keywords.data
        article.is_published = form.is_published.data
        db.session.commit()
        flash('Artículo actualizado exitosamente!', 'success')
        return redirect(url_for('knowledge_base.list_articles'))

    return render_template('knowledge_base/edit.html', form=form, article=article)

# Ruta para eliminar un artículo
@bp.route('/<int:article_id>/delete', methods=['POST'])
@login_required
def delete_article(article_id):
    article = KnowledgeBaseArticle.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    flash('Artículo eliminado exitosamente!', 'danger')
    return redirect(url_for('knowledge_base.list_articles'))
