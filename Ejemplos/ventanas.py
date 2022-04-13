from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pyodbc

class Producto:
    def __init__(self, productoId, nombre, valor):
        self.productoId = productoId
        self.nombre = nombre
        self.valor = valor
    
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


class Aplicacion():
    ventana = 0
    posx_y = 0
        
    def __init__(self):
        self.raiz = Tk()
        self.raiz.geometry('300x200+500+50')
        self.raiz.resizable(0,0)        
        self.raiz.title("Tarea 3 - Sistema de Consulta Clientes y Productos")        
        boton = ttk.Button(self.raiz, text='Abrir', command=self.abrir)
        boton.pack(side=BOTTOM, padx=20, pady=20)
        self.raiz.mainloop()

    def abrir(self):
        ''' Construye una ventana de diálogo '''
        
        self.dialogo = Toplevel()
        Aplicacion.ventana+=1
        Aplicacion.posx_y += 50
        tamypos = '300x400+'+str(Aplicacion.posx_y)+ \
                  '+'+ str(Aplicacion.posx_y)
        self.dialogo.geometry(tamypos)
        #self.dialogo.resizable(0,0)
        ident = self.dialogo.winfo_id()
        titulo = str(Aplicacion.ventana)+": "+str(ident)
        self.dialogo.title(titulo)
        
        # Creating a Frame Container 
        frame = LabelFrame(self.dialogo, text = 'Ingresar Código Producto')
        frame.grid(row = 0, column = 0, columnspan = 2, pady = 20)
        
        # Name Input
        Label(frame, text = 'Código: ').grid(row = 1, column = 0)
        self.code = Entry(frame)
        self.code.focus()
        self.code.grid(row = 1, column = 1)
        
        # Button Add Product 
        ttk.Button(frame, text = 'Buscar Producto', command = buscar_producto ).grid(row = 3, columnspan = 2, sticky = W + E)

        # Output Messages 
        message = Label(self.dialogo, text = '', fg = 'red')
        message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        # Table
        self.tree = ttk.Treeview(self.dialogo, height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Valor', anchor = CENTER)
        
        
        boton = ttk.Button(self.dialogo, text='Cerrar', 
                           command=self.dialogo.destroy)   
        boton.pack(side=BOTTOM, padx=20, pady=20)
                
        self.dialogo.transient(master=self.raiz)
        
        self.dialogo.grab_set()
        self.raiz.wait_window(self.dialogo)
    
        def validation(self):
            return len(self.code.get()) != 0    
    
        def buscar_producto(self):
            
            print("a buscar")        
            if validation():                    
                try:
                    code = int(self.code.get())                
                    print("code:", code)
                    # cleaning Table 
                    records = self.tree.get_children()
                    for element in records:
                        self.tree.delete(element)
                    
                    bd = BaseDatos()
                    producto = bd.TraerProductoPorCodigo(code)
                    
                    if producto is None:
                        self.message['text'] = 'El codigo de producto no existe.!!'    
                    else:
                        self.tree.insert('', 0, text = producto.nombre, values = producto.valor)                    
                        self.message['text'] = ''
                    
                except ValueError:
                    self.message['text'] = 'Error, introduce un numero entero.!'                            
            else:
                self.message['text'] = 'El codigo de producto es Requerido.!!!'
    
def main():
    mi_app = Aplicacion()
    return(0)

if __name__ == '__main__':
    main()