from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from . import mysql
# Para exportar PDF y Excel
from datetime import date
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from openpyxl import Workbook


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')



#PARA PODER GESTIONAR LA BASE DE DATOS ACCEDIENDO CON UN USUARIO Y CONTRASEÑA
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'

class Usuario(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Usuarios WHERE id = %s", (user_id,))
    usuario = cur.fetchone()
    if usuario:
        return Usuario(usuario[0], usuario[1], usuario[2])
    return None

# ---------------------- LOGIN ----------------------

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Usuarios WHERE username = %s", (username,))
        usuario = cur.fetchone()
        if usuario and bcrypt.check_password_hash(usuario[2], password):
            user = Usuario(usuario[0], usuario[1], usuario[2])
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Credenciales inválidas')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


# ---------------------- PRODUCTOS ----------------------
@main.route('/productos')
@login_required
def productos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Producto")
    productos = cur.fetchall()
    return render_template('productos.html', productos=productos)

@main.route('/productos/agregar', methods=['POST'])
def agregar_producto():
    datos = (request.form['nombre'], request.form['descripcion'], request.form['tiempo'], request.form['costo'], request.form['stock'])
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Producto (nombre, descripcion, tiempo_fabricacion, costo_total, stock) VALUES (%s, %s, %s, %s, %s)", datos)
    mysql.connection.commit()
    return redirect(url_for('main.productos'))

@main.route('/productos/eliminar/<int:id>')
def eliminar_producto(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Producto WHERE id_producto = %s", (id,))
    mysql.connection.commit()
    return redirect(url_for('main.productos'))

@main.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        datos = (request.form['nombre'], request.form['descripcion'], request.form['tiempo'], request.form['costo'], request.form['stock'], id)
        cur.execute("UPDATE Producto SET nombre=%s, descripcion=%s, tiempo_fabricacion=%s, costo_total=%s, stock=%s WHERE id_producto=%s", datos)
        mysql.connection.commit()
        return redirect(url_for('main.productos'))
    cur.execute("SELECT * FROM Producto WHERE id_producto = %s", (id,))
    producto = cur.fetchone()
    return render_template('editar_producto.html', producto=producto)


# ---------------------- SERVICIOS ----------------------
@main.route('/servicios')
@login_required
def servicios():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Servicios")
    servicios = cur.fetchall()
    return render_template('servicios.html', servicios=servicios)

@main.route('/servicios/agregar', methods=['POST'])
def agregar_servicio():
    datos = (request.form['nombre'], request.form['costo'], request.form['tiempo'], request.form['descripcion'])
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Servicios (nombre, costo_mano_obra, tiempo_estimado, descripcion) VALUES (%s, %s, %s, %s)", datos)
    mysql.connection.commit()
    return redirect(url_for('main.servicios'))

@main.route('/servicios/eliminar/<int:id>')
def eliminar_servicio(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Servicios WHERE id_servicio = %s", (id,))
    mysql.connection.commit()
    return redirect(url_for('main.servicios'))

@main.route('/servicios/editar/<int:id>', methods=['GET', 'POST'])
def editar_servicio(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        datos = (request.form['nombre'], request.form['costo'], request.form['tiempo'], request.form['descripcion'], id)
        cur.execute("UPDATE Servicios SET nombre=%s, costo_mano_obra=%s, tiempo_estimado=%s, descripcion=%s WHERE id_servicio=%s", datos)
        mysql.connection.commit()
        return redirect(url_for('main.servicios'))
    cur.execute("SELECT * FROM Servicios WHERE id_servicio = %s", (id,))
    servicio = cur.fetchone()
    return render_template('editar_servicio.html', servicio=servicio)

# ---------------------- HERRAMIENTAS ----------------------
@main.route('/herramientas')
@login_required
def herramientas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Herramientas")
    herramientas = cur.fetchall()
    return render_template('herramientas.html', herramientas=herramientas)

@main.route('/herramientas/agregar', methods=['POST'])
def agregar_herramienta():
    datos = (request.form['nombre'], request.form['costo'], request.form['tiempo'], request.form['stock'], request.form['proveedor'])
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Herramientas (nombre, costo, tiempo_adquisicion, stock, id_proveedor) VALUES (%s, %s, %s, %s, %s)", datos)
    mysql.connection.commit()
    return redirect(url_for('main.herramientas'))

@main.route('/herramientas/eliminar/<int:id>')
def eliminar_herramienta(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Herramientas WHERE id_herramienta = %s", (id,))
    mysql.connection.commit()
    return redirect(url_for('main.herramientas'))

@main.route('/herramientas/editar/<int:id>', methods=['GET', 'POST'])
def editar_herramienta(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        datos = (request.form['nombre'], request.form['costo'], request.form['tiempo'], request.form['stock'], request.form['proveedor'], id)
        cur.execute("UPDATE Herramientas SET nombre=%s, costo=%s, tiempo_adquisicion=%s, stock=%s, id_proveedor=%s WHERE id_herramienta=%s", datos)
        mysql.connection.commit()
        return redirect(url_for('main.herramientas'))
    cur.execute("SELECT * FROM Herramientas WHERE id_herramienta = %s", (id,))
    herramienta = cur.fetchone()
    return render_template('editar_herramienta.html', herramienta=herramienta)

# ---------------------- MATERIA PRIMA ----------------------
@main.route('/materia')
@login_required
def materia():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM MateriaPrima")
    materia = cur.fetchall()
    return render_template('materia_prima.html', materia=materia)

@main.route('/materia/agregar', methods=['POST'])
def agregar_materia():
    datos = (request.form['nombre'], request.form['medida'], request.form['especificaciones'], request.form['costo'], request.form['unidad'], request.form['stock'], request.form['proveedor'])
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO MateriaPrima (nombre, medida, especificaciones, costo_unitario, unidad_medida, stock_actual, id_proveedor) VALUES (%s, %s, %s, %s, %s, %s, %s)", datos)
    mysql.connection.commit()
    return redirect(url_for('main.materia'))

@main.route('/materia/eliminar/<int:id>')
def eliminar_materia(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM MateriaPrima WHERE id_materia_prima = %s", (id,))
    mysql.connection.commit()
    return redirect(url_for('main.materia'))

@main.route('/materia/editar/<int:id>', methods=['GET', 'POST'])
def editar_materia(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        datos = (request.form['nombre'], request.form['medida'], request.form['especificaciones'], request.form['costo'], request.form['unidad'], request.form['stock'], request.form['proveedor'], id)
        cur.execute("UPDATE MateriaPrima SET nombre=%s, medida=%s, especificaciones=%s, costo_unitario=%s, unidad_medida=%s, stock_actual=%s, id_proveedor=%s WHERE id_materia_prima=%s", datos)
        mysql.connection.commit()
        return redirect(url_for('main.materia'))
    cur.execute("SELECT * FROM MateriaPrima WHERE id_materia_prima = %s", (id,))
    materia = cur.fetchone()
    return render_template('editar_materia.html', materia=materia)

# ---------------------- CONSUMIBLES ----------------------
@main.route('/consumibles')
@login_required
def consumibles():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Consumibles")
    consumibles = cur.fetchall()
    return render_template('consumibles.html', consumibles=consumibles)

@main.route('/consumibles/agregar', methods=['POST'])
def agregar_consumible():
    datos = (request.form['nombre'], request.form['costo'], request.form['unidad'], request.form['stock'], request.form['proveedor'])
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Consumibles (nombre, costo_unitario, unidad_medida, stock, id_proveedor) VALUES (%s, %s, %s, %s, %s)", datos)
    mysql.connection.commit()
    return redirect(url_for('main.consumibles'))

@main.route('/consumibles/eliminar/<int:id>')
def eliminar_consumible(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Consumibles WHERE id_consumible = %s", (id,))
    mysql.connection.commit()
    return redirect(url_for('main.consumibles'))

@main.route('/consumibles/editar/<int:id>', methods=['GET', 'POST'])
def editar_consumible(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        datos = (request.form['nombre'], request.form['costo'], request.form['unidad'], request.form['stock'], request.form['proveedor'], id)
        cur.execute("UPDATE Consumibles SET nombre=%s, costo_unitario=%s, unidad_medida=%s, stock=%s, id_proveedor=%s WHERE id_consumible=%s", datos)
        mysql.connection.commit()
        return redirect(url_for('main.consumibles'))
    cur.execute("SELECT * FROM Consumibles WHERE id_consumible = %s", (id,))
    consumible = cur.fetchone()
    return render_template('editar_consumible.html', consumible=consumible)

# ---------------------- PROVEEDORES ----------------------
@main.route('/proveedores')
@login_required
def proveedores():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Proveedores")
    proveedores = cur.fetchall()
    return render_template('proveedores.html', proveedores=proveedores)

@main.route('/proveedores/agregar', methods=['POST'])
def agregar_proveedor():
    datos = (request.form['nombre'], request.form['contacto'], request.form['tipo'])
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Proveedores (nombre, contacto, tipo) VALUES (%s, %s, %s)", datos)
    mysql.connection.commit()
    return redirect(url_for('main.proveedores'))

@main.route('/proveedores/eliminar/<int:id>')
def eliminar_proveedor(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Proveedores WHERE id_proveedor = %s", (id,))
    mysql.connection.commit()
    return redirect(url_for('main.proveedores'))

@main.route('/proveedores/editar/<int:id>', methods=['GET', 'POST'])
def editar_proveedor(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        datos = (request.form['nombre'], request.form['contacto'], request.form['tipo'], id)
        cur.execute("UPDATE Proveedores SET nombre=%s, contacto=%s, tipo=%s WHERE id_proveedor=%s", datos)
        mysql.connection.commit()
        return redirect(url_for('main.proveedores'))
    cur.execute("SELECT * FROM Proveedores WHERE id_proveedor = %s", (id,))
    proveedor = cur.fetchone()
    return render_template('editar_proveedor.html', proveedor=proveedor)

# ---------------------- ACTIVOS FIJOS ----------------------
@main.route('/activos')
@login_required
def activos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ActivosFijos")
    activos = cur.fetchall()
    return render_template('activos_fijos.html', activos=activos)

@main.route('/activos/agregar', methods=['POST'])
def agregar_activo():
    datos = (
        request.form['nombre'],
        request.form['valor'],
        request.form['estado'],
        request.form['mantenimiento'],
        request.form['stock']
    )
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO ActivosFijos (nombre, valor_compra, estado, costo_mantenimiento_diario, stock) VALUES (%s, %s, %s, %s, %s)", datos)
    mysql.connection.commit()
    return redirect(url_for('main.activos'))

@main.route('/activos/editar/<int:id>', methods=['GET', 'POST'])
def editar_activo(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        datos = (
            request.form['nombre'],
            request.form['valor'],
            request.form['estado'],
            request.form['mantenimiento'],
            request.form['stock'],
            id
        )
        cur.execute("UPDATE ActivosFijos SET nombre=%s, valor_compra=%s, estado=%s, costo_mantenimiento_diario=%s, stock=%s WHERE id_activo=%s", datos)
        mysql.connection.commit()
        return redirect(url_for('main.activos'))
    cur.execute("SELECT * FROM ActivosFijos WHERE id_activo = %s", (id,))
    activo = cur.fetchone()
    return render_template('editar_activo.html', activo=activo)

@main.route('/activos/eliminar/<int:id>')
def eliminar_activo(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM ActivosFijos WHERE id_activo = %s", (id,))
    mysql.connection.commit()
    return redirect(url_for('main.activos'))

@main.route('/activos/exportar/pdf')
def exportar_activos_pdf():
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
    from reportlab.lib import colors
    from io import BytesIO
    from datetime import date

    cur = mysql.connection.cursor()
    cur.execute("SELECT nombre, valor_compra, estado, costo_mantenimiento_diario, stock FROM ActivosFijos")
    data = cur.fetchall()

    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer)
    contenido = [['Nombre', 'Valor', 'Estado', 'Mantenimiento Diario', 'Stock']] + list(data)
    tabla = Table(contenido)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    pdf.build([tabla])
    buffer.seek(0)
    filename = f"activos_fijos_{date.today()}.pdf"
    return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')

# ---------------------- MOBILIARIO ----------------------
@main.route('/mobiliario')
@login_required
def mobiliario():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Mobiliario")
    mobiliario = cur.fetchall()
    return render_template('mobiliario.html', mobiliario=mobiliario)

@main.route('/mobiliario/agregar', methods=['POST'])
def agregar_mobiliario():
    datos = (
        request.form['nombre'],
        request.form['adquisicion'],
        request.form['mantenimiento'],
        request.form['stock']
    )
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Mobiliario (nombre, costo_adquisicion, costo_mantenimiento_diario, stock) VALUES (%s, %s, %s, %s)", datos)
    mysql.connection.commit()
    return redirect(url_for('main.mobiliario'))

@main.route('/mobiliario/editar/<int:id>', methods=['GET', 'POST'])
def editar_mobiliario(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        datos = (
            request.form['nombre'],
            request.form['adquisicion'],
            request.form['mantenimiento'],
            request.form['stock'],
            id
        )
        cur.execute("UPDATE Mobiliario SET nombre=%s, costo_adquisicion=%s, costo_mantenimiento_diario=%s, stock=%s WHERE id_mobiliario=%s", datos)
        mysql.connection.commit()
        return redirect(url_for('main.mobiliario'))
    cur.execute("SELECT * FROM Mobiliario WHERE id_mobiliario = %s", (id,))
    mobiliario = cur.fetchone()
    return render_template('editar_mobiliario.html', mobiliario=mobiliario)

@main.route('/mobiliario/eliminar/<int:id>')
def eliminar_mobiliario(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Mobiliario WHERE id_mobiliario = %s", (id,))
    mysql.connection.commit()
    return redirect(url_for('main.mobiliario'))

@main.route('/mobiliario/exportar/pdf')
def exportar_mobiliario_pdf():
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
    from reportlab.lib import colors
    from io import BytesIO
    from datetime import date

    cur = mysql.connection.cursor()
    cur.execute("SELECT nombre, costo_adquisicion, costo_mantenimiento_diario, stock FROM Mobiliario")
    data = cur.fetchall()

    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer)
    contenido = [['Nombre', 'Adquisición', 'Mantenimiento Diario', 'Stock']] + list(data)
    tabla = Table(contenido)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    pdf.build([tabla])
    buffer.seek(0)
    filename = f"mobiliario_{date.today()}.pdf"
    return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')

# ---------------------- GASTOS FIJOS ----------------------
@main.route('/gastos')
@login_required
def gastos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM GastosFijos")
    gastos = cur.fetchall()
    return render_template('gastos_fijos.html', gastos=gastos)

@main.route('/gastos/agregar', methods=['POST'])
def agregar_gasto():
    datos = (request.form['tipo'], request.form['monto'])
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO GastosFijos (tipo, monto_diario) VALUES (%s, %s)", datos)
    mysql.connection.commit()
    return redirect(url_for('main.gastos'))

@main.route('/gastos/editar/<int:id>', methods=['GET', 'POST'])
def editar_gasto(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        datos = (request.form['tipo'], request.form['monto'], id)
        cur.execute("UPDATE GastosFijos SET tipo=%s, monto_diario=%s WHERE id_gasto=%s", datos)
        mysql.connection.commit()
        return redirect(url_for('main.gastos'))
    cur.execute("SELECT * FROM GastosFijos WHERE id_gasto = %s", (id,))
    gasto = cur.fetchone()
    return render_template('editar_gasto.html', gasto=gasto)

@main.route('/gastos/eliminar/<int:id>')
def eliminar_gasto(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM GastosFijos WHERE id_gasto = %s", (id,))
    mysql.connection.commit()
    return redirect(url_for('main.gastos'))

# --------------------- Usuarios ---------------
