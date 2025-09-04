arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print('Valores que estan en el arreglo: ')
for i in range (len(arr)):
    print(f"Indice {i} :{arr[i]}")
n = int(input('¿Que numero quiere ingresar?'))
posi = int(input('¿En que posicion quieres que la ponga?'))
arr.insert(posi, n)
print('\nYa actualizado:')
for i in range(len(arr)):
    print(f"Índice {i} : {arr[i]}")