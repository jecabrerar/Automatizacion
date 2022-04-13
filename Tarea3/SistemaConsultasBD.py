from msilib.schema import Class
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
import pyodbc
from itertools import cycle
    
class Producto:
    def __init__(self, productoId, nombre, valor):
        self.productoId = productoId
        self.nombre = nombre
        self.valor = valor
        
class RutResult:
    
    def __init__(self, rutN, digito, esValido):
        self.RutN = rutN
        self.Digito = digito
        self.EsValido = esValido
        
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
    
class Aplicacion:
    
    def validarRut(self, rut):
        rut = rut.upper()
        rut = rut.replace("-","")
        rut = rut.replace(".","")
        aux = rut[:-1]
        dv = rut[-1:]
    
        revertido = map(int, reversed(str(aux)))
        factors = cycle(range(2,8))
        s = sum(d * f for d, f in zip(revertido,factors))
        res = (-s)%11
        
        rutValido = None
        if str(res) == dv:
            rutValido =  True
        elif dv=="K" and res==10:
            rutValido = True
        else:
            rutValido = False
        
        return RutResult(aux, dv, rutValido)
        
        
    def __init__(self, window):
        
        window.geometry("450x450") 
        # Initializations 
        self.wind = window
        self.wind.title('Sistema Consulta Productos y Clientes')
        #self.wind.eval('tk::PlaceWindow . center')                           
        
        def cerrar_window():
            valor = messagebox.askquestion("Salir","¿Deseas salir de la aplicación?")
            if valor == "yes":
                window.destroy()
        
        menus = Menu(window)
        col1 = Menu(menus, tearoff=0)
        col1.add_command(label="Consultar Producto", command = self.consultar_producto)
        col1.add_command(label="Consultar Cliente", command=self.consultar_cliente)
        col1.add_separator()
        col1.add_command(label="Cerrar", command=cerrar_window)
        menus.add_cascade(label="Archivo", menu=col1)
        window.config(menu=menus)
        
    def consultar_cliente(self):
        
        def buscar_cliente():
            print("Buscar Cliente")
            try:
                rutCli = self.rut.get()
                
                rutObj = self.validarRut(rutCli)
                
                if ( rutObj.EsValido ==False ):
                    self.messageCli['text'] = 'El rut ingresado es invalido.!!'
                    return
                
                rutN = int(rutObj.RutN)
                print("rut:", rutN)
                
                # cleaning Table 
                rows = self.treeVts.get_children()
                for element in rows:
                    self.treeVts.delete(element)
                    
                self.lblApeMat['text'] = ''
                self.lblApePat['text'] = ''
                self.lblNombre['text'] = ''
                self.lblFecNac['text'] = ''
                                    
                bd = BaseDatos()
                cliente = bd.TraerClientePorRut(rutN)
                
                if cliente is None:
                    self.messageCli['text'] = 'El rut ingresado no existe.!!'                        
                else:
                    self.lblNombre['text'] = str(cliente.nombre)
                    self.lblApePat['text'] = str(cliente.apePat)
                    self.lblApeMat['text'] = str(cliente.apeMat)
                    self.lblFecNac['text'] = str(cliente.fechaNac)
                                            
                    listaVentas =  bd.TraerVentasCliente(cliente.clienteId)
                                            
                    for vnta in listaVentas:                                                    
                        self.treeVts.insert('', END, text = vnta.ProductoId ,
                            values = (vnta.NombreProducto, 
                                        vnta.Cantidad, 
                                        str('{:,}'.format(vnta.ValorVenta).replace(',', '.')), 
                                        vnta.FechaVenta))
                                                    
                    self.messageCli['text'] = ''
                        
            except ValueError:
                self.messageCli['text'] = 'Error, introduce un numero entero.!'
                    
        
        #self.windCli = Toplevel()
        self.windCli = Toplevel(self.wind)        
        self.windCli.geometry("450x380")         
        self.windCli.title('Consultar Cliente')
        #self.windCli.eval('tk::PlaceWindow . center')
        
                            
        # Creating a Frame Container 
        self.frame1 = LabelFrame(self.windCli, text = 'Ingresar RUT Cliente con/sin puntos y guion', width=400, height=80)
        self.frame1.grid(row = 0, column = 0, columnspan=2, sticky=W + E, \
             padx=5, pady=0, ipadx=0, ipady=0)
        
        # Name Input
        Label(self.frame1, text = 'RUT: ').grid(row = 1, column = 0)
        self.rut = Entry(self.frame1)
        self.rut.focus()
        self.rut.grid(row = 1, column = 1)
        
        # Button Add Product 
        Button(self.frame1, text = 'Buscar Cliente', command=buscar_cliente).grid(row = 1, columnspan = 2, column=2, sticky = W + E)

        # Output Messages 
        self.messageCli = Label(self.windCli, text = '', fg = 'red')
        self.messageCli.grid(row = 2, column = 0, columnspan = 2, sticky = W + E)
                
        # Creating a Frame Container Cliente
        self.frameCli = LabelFrame(self.windCli, text = '', width=400, height=80)
        self.frameCli.grid(row = 3, column = 0, columnspan=2, sticky=W + E, \
             padx=5, pady=0, ipadx=0, ipady=0)
                
        Label(self.frameCli, text = 'Nombre                   :').grid(row = 4, column = 0, sticky = W)
        self.lblNombre = Label(self.frameCli, text = '')
        self.lblNombre.grid(row = 4, column = 1, columnspan = 2, sticky = W)        
        
        Label(self.frameCli, text = 'Apellido Paterno    :').grid(row = 5, column = 0, sticky = W)
        self.lblApePat = Label(self.frameCli, text = '')
        self.lblApePat.grid(row = 5, column = 1, columnspan = 2, sticky = W)
        
        Label(self.frameCli, text = 'Apellido Materno   :').grid(row = 6, column = 0, sticky = W)
        self.lblApeMat = Label(self.frameCli, text = '')
        self.lblApeMat.grid(row = 6, column = 1, columnspan = 2, sticky = W)
        
        Label(self.frameCli, text = 'Fecha Nacimiento  :').grid(row = 7, column = 0, sticky = W)
        self.lblFecNac = Label(self.frameCli, text = '')
        self.lblFecNac.grid(row = 7, column = 1, columnspan = 2, sticky = W)
                        
        # Creating a Frame Container Ventas
        self.frameVentas = LabelFrame(self.windCli, text = '')
        self.frameVentas.grid(row = 8, column = 0, columnspan = 2, pady = 5)

        # Table
        self.treeVts = Treeview(self.frameVentas, height = 9, columns=("col1","col2","col3", "col4"))
        self.treeVts.grid(row = 1, column = 6)
        self.treeVts.column("#0", width=55)
        self.treeVts.column("col1", width=120)
        self.treeVts.column("col2", width=70)
        self.treeVts.column("col3", width=80, anchor = E)
        self.treeVts.column("col4", width=120)
        
        self.treeVts.heading('#0', text = 'Id Venta')
        self.treeVts.heading('col1', text = 'Nombre Producto')
        self.treeVts.heading('col2', text = 'Cantidad')
        self.treeVts.heading('col3', text = 'Valor Venta')
        self.treeVts.heading('col4', text = 'Fecha Venta')
                
        self.windCli.grab_set()
        self.windCli.wait_window(self.windCli)
        
        
    def consultar_producto(self):
        
        def validation():
            print("validando")
            return len(self.code.get()) != 0 
        
        def buscar_producto():
            print("a buscar")
            if validation():                    
                try:
                    codeProduct = int(self.code.get())                
                    print("code:", codeProduct)
                    # cleaning Table 
                    records = self.tree.get_children()
                    for element in records:
                        self.tree.delete(element)
                    
                    bd = BaseDatos()
                    producto = bd.TraerProductoPorCodigo(codeProduct)
                    
                    if producto is None:
                        self.message['text'] = 'El codigo de producto no existe.!!'                        
                    else:
                        self.tree.insert('', END, text = producto.productoId, values = (producto.nombre, str('{:,}'.format(producto.valor).replace(',', '.'))))
                        self.message['text'] = ''
                    
                except ValueError:
                    self.message['text'] = 'Error, introduce un numero entero.!'
                    
            else:
                self.message['text'] = 'El codigo de producto es Requerido.!!!'                
        
        #newWindow = Tk()
        self.newWindow = Toplevel()
        self.newWindow.geometry("450x380")        
        self.newWindow.title('Consultar Producto')
        
                            
        # Creating a Frame Container 
        self.frame = LabelFrame(self.newWindow, text = 'Ingresar Código Producto', width=400, height=80)
        self.frame.grid(row = 0, column = 0, columnspan = 2, pady = 20, sticky=W + E)
        
        # Name Input
        Label(self.frame, text = 'Código: ').grid(row = 1, column = 0)
        self.code = Entry(self.frame)
        self.code.focus()
        self.code.grid(row = 1, column = 1)
        
        # Button Add Product 
        Button(self.frame, text = 'Buscar Producto', command=buscar_producto).grid(row = 1, column=2, columnspan = 2, sticky = W + E)

        # Output Messages 
        self.message = Label(self.newWindow, text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, sticky = W + E)

        # Table
        self.tree = Treeview(self.newWindow, height = 10, columns = ("col1","col2"))
        self.tree.grid(row = 4, column = 0)        
        self.tree.column("#0", width=70, anchor = W)
        self.tree.column("col1", width=200, anchor = W)
        self.tree.column("col2", width=90, anchor = E)
        
        self.tree.heading('#0', text = 'Id Producto')
        self.tree.heading('col1', text = 'Nombre')
        self.tree.heading('col2', text = 'Precio')
        
        self.newWindow.grab_set()
        self.newWindow.wait_window(self.newWindow)
        
            
#bloque princial

window = Tk()
app = Aplicacion(window) 
window.mainloop()








 



