am = []
pm = []
x = 0

for x in range(4):
    sueldoam = int(input("ingrese sueldo " + str(x+1) + " del turno AM: "))
    am.append(sueldoam)
    sueldopm = int(input("ingrese sueldo " + str(x+1) + " del turno PM: "))
    pm.append(sueldopm)

print("Sueldos turnos AM")
print(am)
print("Sueldos turnos PM")
print(pm)