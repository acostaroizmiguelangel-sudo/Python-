def burbu(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

datos = []
print("Hola, ingrese 5 números y serán ordenados:")

for i in range(5):
    numero = int(input(f"Ingrese el número {i + 1}: "))
    datos.append(numero)

print("\nEstos son los datos antes de ordenar:")
print(datos)

burbu(datos)

print("Estos son los datos después de ordenar:")
print(datos)
