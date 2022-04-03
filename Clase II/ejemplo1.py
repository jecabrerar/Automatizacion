altura = []
promedio = 0 
altas = 0
bajas = 0
x = 0
total = 0

for x  in range(5):
    valor = float(input("Ingrese la estatura de la persona " + str(x+1) + ": "))
    altura.append(valor)
    total += valor

promedio = total / 5
x = 0

for x in range(5):
    if altura[x] > promedio:
        altas = altas +1
    elif altura[x] < promedio:
        bajas = bajas +1
print("El promedio de estatura es: ", promedio)
print("El numero de personas altas con respecto al promedio son:", altas)
print("El numero de personas bajas con respecto al promedio son:", bajas)




