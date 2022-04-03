nombres = []


for x in range(5):
    nombre = input("Ingrese el nombre "+ str(x+1) + " :")
    nombres.append(nombre)

menor = nombres[0]

for x in range(1, 5):
    if nombres[x] < menor:
        menor = nombres[x]
    
print(nombres)
print(menor)
