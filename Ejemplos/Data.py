import pyodbc

class Producto:
    def __init__(self, productoId, nombre, valor):
        self.productoId = productoId
        self.nombre = nombre
        self.valor = valor
        
class Cliente:
    def __init__(self, clienteId, rut, dv, nombre, apePat, apeMat, fechaNac):
        self.clienteId = clienteId
        self.rut = rut
        self.dv = dv
        self.nombre = nombre
        self.apePat = apePat
        self.apeMat = apeMat
        self.fechaNac = fechaNac
        
class Venta:
    def __init__(self, VentaId, ProductoId, NombreProducto, ClienteId, Cantidad, ValorVenta, FechaVenta):
        self.VentaId = VentaId
        self.ProductoId = ProductoId
        self.NombreProducto = NombreProducto
        self.ClienteId = ClienteId
        self.Cantidad = Cantidad
        self.ValorVenta = ValorVenta
        self.FechaVenta = FechaVenta
    
        
class BaseDatos:

    stringConnection =  'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-T8N6TK6\SQLEXPRESS;DATABASE=BD_AUTOMATIZACION_TAREA3;Trusted_Connection=yes;'
            
    def TraerProductoPorCodigo(self, productoId):        
        cnn = pyodbc.connect(self.stringConnection)
        cursor1 = cnn.cursor()
        cursor1.execute("select productoId, nombre, valor from Productos where productoId = " + str(productoId))
                
        row = cursor1.fetchone()
        producto = None
        
        if row is not None:
            producto = Producto(row[0], row[1], row[2])
        
        cursor1.close()
        cnn.close()       
        
        return producto
    
    def TraerClientePorRut(self, rutN):        
        cnn = pyodbc.connect(self.stringConnection)
        cursor1 = cnn.cursor()
        cursor1.execute("select ClienteId, Rut, Dv, Nombre, ApePat, ApeMat, FechaNacimiento from Clientes where rut = " + str(rutN))
                
        row = cursor1.fetchone()
        cliente = None
        
        if row is not None:
            cliente = Cliente(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        
        cursor1.close()
        cnn.close()       
        
        return cliente
    
    def TraerVentasCliente(self, clienteId):        
        cnn = pyodbc.connect(self.stringConnection)
        cursor1 = cnn.cursor()
        cursor1.execute("select a.VentaId, a.ProductoId, b.Nombre, a.ClienteId, a.Cantidad, a.ValorVenta, a.FechaVenta from  Ventas a inner join Productos b on a.ProductoId = b.ProductoId where ClienteId = " + str(clienteId) + " order by a.VentaId")
                
        db_rows = cursor1.fetchall()
        ventas = []
        
        for row in db_rows:
            venta = Venta(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            ventas.append(venta)
        
        cursor1.close()
        cnn.close()       
        
        return ventas
    
class Repository:
        
    db = None
        
    def __init__(self):
        self.db = BaseDatos()
    
    def GetCliente(self, rutN):
        return self.db.TraerClientePorRut(rutN)
    
    def GetProducto(self, proId):
        return self.db.TraerProductoPorCodigo(proId)
    
    def GetVentasCliente(self, cliId):
        return self.db.TraerVentasCliente(cliId)