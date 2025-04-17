from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required
from app import db
from app.models import CostCenter
from app.utils.cost_center_forms import CostCenterForm
import pandas as pd
import uuid
from openpyxl import load_workbook
from io import BytesIO

bp = Blueprint('cost_center', __name__, url_prefix='/cost_center')

# Ruta para listar todos los Centro Costo
@bp.route('/list')
@login_required
def list_cost_center():
    cost_centers = CostCenter.query.filter_by(active=1).all()  # Obtener todos los Centro Costo
    return render_template('cost_center/list.html', cost_centers=cost_centers)

# Ruta para ver los detalles de un centro_costo
@bp.route('/<int:cost_center_id>/details')
@login_required
def cost_center_details(cost_center_id):
    cost_center = CostCenter.query.get_or_404(cost_center_id)  # Obtener el centro_costo por su ID
    return render_template('cost_center/details.html', cost_center=cost_center)

# Ruta para crear un nuevo centro_costo
@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_cost_center():
    form = CostCenterForm()

    if form.validate_on_submit():
        # Crear un nuevo centro_costo
        cost_center = CostCenter(
            name=form.name.data,
            branch=form.branch.data,
            location=form.location.data,
            id_number=form.id_number.data,
            management=form.management.data,
            manager=form.manager.data,
            email_manager=form.email_manager.data,
            administrator=form.administrator.data,
            administrator_email=form.administrator_email.data,
            administrator_cellphone=form.administrator_cellphone.data,
        )
        db.session.add(cost_center)
        db.session.commit()
        flash('centro_costo creado exitosamente!', 'success')
        return redirect(url_for('cost_center.list_cost_centers'))

    return render_template('cost_center/create.html', form=form)




@bp.route('/upload-cost-center', methods=['POST'])
def upload_cost_centers():
    archivo = request.files.get('archivo')
    if not archivo or not archivo.filename.endswith('.xlsx'):
        flash('Por favor, sube un archivo .xlsx válido.', 'warning')
        return redirect(url_for('cost_center.list_cost_center'))
    try:
         # Verificamos que sea un archivo Excel válido con openpyxl
        workbook = load_workbook(filename=BytesIO(archivo.read()))
        archivo.seek(0)  # Reiniciamos el puntero para que pandas pueda leer el archivo también
        df = pd.read_excel(archivo)
        columnas_requeridas = {"CC", "NOMBRE-CC", "Sucursal", "Faena", "Gerencia","Gerente", "Correo-Gerente", "Administrador", "Correo-Administrador", "Celular-Administrador"}
        if not columnas_requeridas.issubset(df.columns):
            faltantes = columnas_requeridas - set(df.columns)
            flash(f'Faltan columnas requeridas: {", ".join(faltantes)}', 'danger')
            return redirect(url_for('cost_center.list_cost_center'))
        for _, row in df.iterrows():
            nuevo_centro_costo = CostCenter(
                uuid=str(uuid.uuid4()),
                id_number=row['CC'],
                name=row['NOMBRE-CC'],
                branch=row['Sucursal'],
                location=row['Faena'],
                management=row['Gerencia'],
                manager=row['Gerente'],
                email_manager=row['Correo-Gerente'],
                administrator=row['Administrador'],
                administrator_email=row['Correo-Administrador'],
                administrator_cellphone=row['Celular-Administrador'],
            )
            db.session.add(nuevo_centro_costo)
        db.session.commit()
        flash('Centro Costo cargados correctamente.', 'success')
    except Exception as e:
            flash(f'Error al procesar el archivo: {e}', 'danger')
    return redirect(url_for('cost_center.list_cost_center'))

@bp.route('/cost_centers/download', methods=['GET'])
def download_cost_centers_excel():
    cost_centers = CostCenter.query.all()

    data = [{
        "CC": cc.code,
        "NOMBRE-CC": cc.name,
        "Sucursal": cc.branch,
        "Faena": cc.site,
        "Gerencia": cc.management,
        "Gerente": cc.manager,
        "Correo-Gerente": cc.manager_email,
        "Administrador": cc.admin,
        "Correo-Administrador": cc.admin_email,
        "Celular-Administrador": cc.admin_phone,
    } for cc in cost_centers]

    df = pd.DataFrame(data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='CostCenters')

    output.seek(0)

    return send_file(output,
                     as_attachment=True,
                     download_name="cost_centers.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

