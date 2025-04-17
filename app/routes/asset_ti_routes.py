from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Asset, Software
from app.utils.asset_ti_forms import AssetForm

bp = Blueprint('asset_ti', __name__, url_prefix='/asset_ti')

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_asset():
    form = AssetForm()
    
    if form.validate_on_submit():
        # Crear un nuevo asset
        asset = Asset(
            name=form.name.data,
            asset_type=form.asset_type.data,
            model=form.model.data,
            serial_number=form.serial_number.data,
            purchase_date=form.purchase_date.data,
            warranty_expiration=form.warranty_expiration.data,
            status=form.status.data,
            location=form.location.data,
            notes=form.notes.data
        )
        
        # Si el asset es de tipo Software, agregamos los campos adicionales
        if form.asset_type.data == 'software':
            software = Software(
                name=form.name.data,
                asset_type=form.asset_type.data,
                model=form.model.data,
                serial_number=form.serial_number.data,
                purchase_date=form.purchase_date.data,
                warranty_expiration=form.warranty_expiration.data,
                status=form.status.data,
                location=form.location.data,
                notes=form.notes.data,
                license_key=form.license_key.data,
                license_expiration=form.license_expiration.data,
                version=form.version.data
            )
            db.session.add(software)
        else:
            db.session.add(asset)

        # Confirmar y redirigir
        db.session.commit()
        flash('Asset creado exitosamente', 'success')
        return redirect(url_for('asset_ti.create_asset'))
    
    return render_template('asset_ti/create.html', form=form)

@bp.route('/list')
@login_required
def list_assets():
    assets = Asset.query.all()  # Obtener todos los assets
    return render_template('asset_ti/list.html', assets=assets)

# Ruta para ver los detalles de un asset
@bp.route('/<int:asset_id>/details')
@login_required
def asset_details(asset_id):
    asset = Asset.query.get_or_404(asset_id)  # Obtener el asset por su ID
    if isinstance(asset, Software):  # Si es un software, mostramos sus atributos extra
        return render_template('asset_ti/details_software.html', asset=asset)
    return render_template('asset_ti/details.html', asset=asset)