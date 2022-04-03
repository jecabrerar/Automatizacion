nombres = []
notas = []
for x in range(3):
    nom = input("Ingrese el nombre del alumno:")
    nombres.append(nom)
    no1 = int(input("Ingrese la primer nota:"))
    no2 = int(input("Ingrese la segunda nota:"))
    notas.append([no1,no2])

for x in range(3):
    print(nombres[x], notas[x][0], notas[x][1])