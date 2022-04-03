
from ast import Str
from cgi import print_form
import os

def pedirNumeroEntero(mensaje):
    correcto = False
    num = 0
    while(not correcto):
        try:
            num = int(input(mensaje))
            correcto=True
        except ValueError:
            print('Error, introduce un numero entero')
     
    return num

def Menu():
    print("*** V E N T A  -  P R O D U C T O S  -  F E R R E T E R I A  ***")
    print("# PRODUCTO           PRECIO")
    print("_______________________________________________")
    for i in range(len(productos)):        
        nombre = productos[i][0]
        valor = productos[i][1]        
        print(str(i+1).ljust(3) + nombre.ljust(lGlosa) +  "$" + str('{:,}'.format(valor).replace(',', '.')))

    print("_______________________________________________")

def ResumenCarroCompra():
    
    print("*** RESUMEN COMPRAS INGRESADAS ***")
    print("  PRODUCTO        PRECIO       CANTIDAD    SUBTOTAL")
    print("____________________________________________________")

    total = 0
    for x in range(len(compras)):
        nomProd = compras[x][0]
        valorProd = compras[x][1]
        cantidad = compras[x][2]
        subtotal = valorProd * cantidad

        total = total + (valorProd * cantidad)
        print(nomProd.ljust(lGlosa) + "$" +  str('{:,}'.format(valorProd).replace(',', '.')).ljust(12) + str(cantidad).ljust(10) + "$" +  str('{:,}'.format(subtotal).replace(',', '.')).ljust(12))

    print("____________________________________________________")
    print("TOTAL DE PRODUCTOS COMPRADOS: ".ljust(42) + "$" + str('{:,}' .format(total).replace(',', '.') ))

    return total


despachos = [["La Florida", 3500], ["Maipu", 5500], ["La Pintana", 7500], ["San Bernardo", 8000], ["Puente Alto", 6500]]
productos = [["Martillo", 8500], ["Brocha", 3500], ["Taladro", 45000], ["Palas", 18590]]
compras = []
valor = 0
producto = ""
espacios = 0
lGlosa = 18 

comprando = "S"
seleccionValida = False
os.system('cls')

while comprando == "S":
    Menu()
    
    while seleccionValida == False:
        
        seleccion = pedirNumeroEntero("Ingrese codigo producto a comprar: ")
        if (seleccion > len(productos)):
            print("Error, ingrese un codigo de producto valido.")
        else:
            seleccionValida = True

    producto = productos[seleccion-1][0]
    valorProducto = productos[seleccion-1][1]

    print("Producto Seleccionado: " + producto)    
    print("")
    
    cantidad = pedirNumeroEntero("Ingrese que cantiad "+ producto +" que desea comprar: ")
    
    venta = [producto, valorProducto, cantidad]
    
    compras.append(venta)
    
    comprando = input("¿Si desea seguir comprando ? digite s/n: ")
    comprando = comprando.upper()
    seleccionValida = False
    os.system('cls')

os.system('cls')

total = ResumenCarroCompra()

print("")

despacho = input("¿Desea despacho? digite s/n: ")
valorDespacho = 0

if despacho.upper() == "S":
    print("TARIFAS PARA EL DESPACHO")
    print("  PRODUCTO        PRECIO")
    print("____________________________________")
    for j in range(len(despachos)):
        comuna = despachos[j][0]
        valorDespacho =  despachos[j][1]
        print(str(j+1).ljust(3) + comuna.ljust(lGlosa) + str('{:,}'.format(valorDespacho).replace(',', '.') ).ljust(10))
    print("____________________________________")

    seleccionValida = False
    while seleccionValida == False:
        
        seleccion = pedirNumeroEntero("Ingrese codigo comuna destino para despacho: ")
        if (seleccion > len(despachos)):
            print("Error, ingrese un codigo de producto valido.")
        else:
            seleccionValida = True
        
    total = ResumenCarroCompra()
    comuna = despachos[seleccion-1][0]
    valorDespacho = despachos[seleccion-1][1]

    print("")
    print("DESTINO DESPACHO    : " + comuna )
    print("VALOR  DESPACHO     : $" + str('{:,}'.format(valorDespacho).replace(',', '.') ) )
    
print("")
total_Pagar = total + valorDespacho
print("TOTAL A PAGAR --> $" + str('{:,}'.format(total_Pagar).replace(',', '.') ))
print("")
print("¡¡¡ GRACIAS POR SU COMPRA !!!")
print("")




