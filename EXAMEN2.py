def ordenar(lista):
    n = len(lista)
  
    for i in range(n):
       
        for j in range(0, n - i - 1):
            
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
matriz = [
    [8, 1, 6],
    [3, 5, 7],
    [4, 9, 2]
]

print(matriz)
for fila in matriz:
    ordenar(fila)
print(matriz)