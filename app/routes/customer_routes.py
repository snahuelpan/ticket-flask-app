from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required
from app import db
from app.models import Customer
from app.utils.customer_forms import CustomerForm
import pandas as pd
import uuid
from openpyxl import load_workbook
from io import BytesIO

bp = Blueprint('customer', __name__, url_prefix='/customer')

# Ruta para listar todos los clientes
@bp.route('/list')
@login_required
def list_customers():
    customers = Customer.query.filter_by(active=1).all()  # Obtener todos los clientes
    return render_template('customer/list.html', customers=customers)

# Ruta para ver los detalles de un cliente
@bp.route('/<int:customer_id>/details')
@login_required
def customer_details(customer_id):
    customer = Customer.query.get_or_404(customer_id)  # Obtener el cliente por su ID
    return render_template('customer/details.html', customer=customer)

# Ruta para crear un nuevo cliente
@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_customer():
    form = CustomerForm()

    if form.validate_on_submit():
        # Crear un nuevo cliente
        customer = Customer(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data
        )
        db.session.add(customer)
        db.session.commit()
        flash('Cliente creado exitosamente!', 'success')
        return redirect(url_for('customer.list_customers'))

    return render_template('customer/create.html', form=form)


@bp.route('/list/upgrade')
@login_required
def list_upgrade_customers():
    #customers = Customer.query.all()  # Obtener todos los clientes
    customer = Customer()
    customers = customer.get_all_users()
    return customers
    return render_template('customer/list.html', customers=customers)


@bp.route('/upload-customers', methods=['POST'])
def upload_customers():
    archivo = request.files.get('archivo')
    if not archivo or not archivo.filename.endswith('.xlsx'):
        flash('Por favor, sube un archivo .xlsx válido.', 'warning')
        return redirect(url_for('customer.list_customers'))
    try:
         # Verificamos que sea un archivo Excel válido con openpyxl
        workbook = load_workbook(filename=BytesIO(archivo.read()))
        archivo.seek(0)  # Reiniciamos el puntero para que pandas pueda leer el archivo también
        df = pd.read_excel(archivo)
        columnas_requeridas = {"Nombre", "Apellido", "Rut", "Centro-Costo", "Cargo", "Email"}
        if not columnas_requeridas.issubset(df.columns):
            faltantes = columnas_requeridas - set(df.columns)
            flash(f'Faltan columnas requeridas: {", ".join(faltantes)}', 'danger')
            return redirect(url_for('customer.list_customers'))
        for _, row in df.iterrows():
            nuevo_cliente = Customer(
                uuid=str(uuid.uuid4()),
                name=row['Nombre'],
                lastname=row['Apellido'],
                id_number=row['Rut'],
                cost_center=row['Centro-Costo'],
                job_title=row['Cargo'],
                email=row['Email']
            )
            db.session.add(nuevo_cliente)
        db.session.commit()
        flash('Clientes cargados correctamente.', 'success')
    except Exception as e:
            flash(f'Error al procesar el archivo: {e}', 'danger')
    return redirect(url_for('customer.list_customers'))


@bp.route('/customers/download', methods=['GET'])
def download_customers_excel():
    customers = Customer.query.all()

    data = [{
        "RUT": c.id_number,
        "Nombre": f"{c.name} {c.lastname}",
        "CC": c.cost_center,
        "Cargo": c.job_title,
        "Email": c.email
    } for c in customers]

    df = pd.DataFrame(data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Trabajadores')

    output.seek(0)

    return send_file(output,
                     as_attachment=True,
                     download_name="trabajadores.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")