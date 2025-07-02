
-- Base de datos para gestión de inventario, producción y cotizaciones

CREATE DATABASE IF NOT EXISTS fabrica_racks;
USE fabrica_racks;

-- Tabla de Proveedores
CREATE TABLE Proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    contacto TEXT,
    tipo ENUM('Materia Prima', 'Consumible', 'Herramienta')
);

-- Tabla de Materia Prima
CREATE TABLE MateriaPrima (
    id_materia_prima INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    medida VARCHAR(50),
    especificaciones TEXT,
    costo_unitario DECIMAL(10,2),
    unidad_medida VARCHAR(20),
    stock_actual FLOAT,
    id_proveedor INT,
    FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor)
);

-- Tabla de Consumibles
CREATE TABLE Consumibles (
    id_consumible INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    costo_unitario DECIMAL(10,2),
    unidad_medida VARCHAR(20),
    stock INT,
    id_proveedor INT,
    FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor)
);

-- Tabla de Herramientas
CREATE TABLE Herramientas (
    id_herramienta INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    costo DECIMAL(10,2),
    tiempo_adquisicion VARCHAR(50),
    stock INT,
    id_proveedor INT,
    FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor)
);

-- Tabla de Productos
CREATE TABLE Producto (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    tiempo_fabricacion TIME,
    costo_total DECIMAL(10,2),
    stock INT
);

-- Producto - Materia Prima
CREATE TABLE ProductoMateriaPrima (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT,
    id_materia_prima INT,
    cantidad FLOAT,
    FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
    FOREIGN KEY (id_materia_prima) REFERENCES MateriaPrima(id_materia_prima)
);

-- Producto - Consumible
CREATE TABLE ProductoConsumible (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT,
    id_consumible INT,
    cantidad FLOAT,
    FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
    FOREIGN KEY (id_consumible) REFERENCES Consumibles(id_consumible)
);

-- Producto - Herramienta
CREATE TABLE ProductoHerramienta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT,
    id_herramienta INT,
    tiempo_utilizado TIME,
    FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
    FOREIGN KEY (id_herramienta) REFERENCES Herramientas(id_herramienta)
);

-- Servicios
CREATE TABLE Servicios (
    id_servicio INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    costo_mano_obra DECIMAL(10,2),
    tiempo_estimado TIME,
    descripcion TEXT
);

-- Servicio - Producto
CREATE TABLE ServicioProducto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_servicio INT,
    id_producto INT,
    cantidad FLOAT,
    FOREIGN KEY (id_servicio) REFERENCES Servicios(id_servicio),
    FOREIGN KEY (id_producto) REFERENCES Producto(id_producto)
);

-- Servicio - Consumible
CREATE TABLE ServicioConsumible (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_servicio INT,
    id_consumible INT,
    cantidad FLOAT,
    FOREIGN KEY (id_servicio) REFERENCES Servicios(id_servicio),
    FOREIGN KEY (id_consumible) REFERENCES Consumibles(id_consumible)
);

-- Servicio - Herramienta
CREATE TABLE ServicioHerramienta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_servicio INT,
    id_herramienta INT,
    tiempo_utilizado TIME,
    FOREIGN KEY (id_servicio) REFERENCES Servicios(id_servicio),
    FOREIGN KEY (id_herramienta) REFERENCES Herramientas(id_herramienta)
);

-- Transporte
CREATE TABLE Transporte (
    id_transporte INT AUTO_INCREMENT PRIMARY KEY,
    descripcion TEXT,
    costo_km DECIMAL(10,2),
    capacidad_carga FLOAT
);

-- Cotizaciones
CREATE TABLE Cotizacion (
    id_cotizacion INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE,
    cliente VARCHAR(100),
    descripcion TEXT,
    tiempo_fabricacion_estimado TIME,
    tiempo_entrega_estimado TIME,
    costo_total DECIMAL(10,2),
    observaciones TEXT
);

-- Detalle de Cotización
CREATE TABLE DetalleCotizacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cotizacion INT,
    tipo_item ENUM('producto', 'servicio'),
    id_item INT,
    cantidad INT,
    subtotal DECIMAL(10,2),
    FOREIGN KEY (id_cotizacion) REFERENCES Cotizacion(id_cotizacion)
);

-- Gastos Fijos
CREATE TABLE GastosFijos (
    id_gasto INT AUTO_INCREMENT PRIMARY KEY,
    tipo ENUM('Luz', 'Agua', 'Gas', 'Renta'),
    monto_diario DECIMAL(10,2)
);

-- Activos Fijos
CREATE TABLE ActivosFijos (
    id_activo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    valor_compra DECIMAL(10,2),
    estado ENUM('Bueno', 'Regular', 'Malo'),
    costo_mantenimiento_diario DECIMAL(10,2),
    stock INT
);

-- Mobiliario
CREATE TABLE Mobiliario (
    id_mobiliario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    costo_adquisicion DECIMAL(10,2),
    costo_mantenimiento_diario DECIMAL(10,2),
    stock INT
);

CREATE TABLE Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
INSERT INTO Usuarios (username, password)
VALUES ('Conta1', '	Israel72!');