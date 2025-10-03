def promedio(lista):
    
    total = 0
    for num in lista:
       
        total += num
    
    if len(lista) > 0:
        return total / len(lista)
    else:
        return 0


matriz = [
    [8, 1, 6],
    [3, 5, 7],
    [4, 9, 2]
]
print("Esta es la matriz:")
print(matriz)

print("\nPromedio de cada fila:")
for fila in matriz:
    
    print(promedio(fila))