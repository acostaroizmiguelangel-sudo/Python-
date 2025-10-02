import random

def swap(a, j, k): 
    a[j], a[k] = a[k], a[j] 

def partition(a, l, h):

    pvt = a[h]
    j = l - 1
    for k in range(l, h): 
        if a[k] <= pvt: 
            j += 1
            swap(a, j, k)
    swap(a, j + 1, h)
    return j + 1

def quicksort(a, l, h): 
    if l < h: 
        pi = partition(a, l, h)
        quicksort(a, l, pi - 1)
        quicksort(a, pi + 1, h)

numeros = [random.randint(1, 100) for _ in range(20)]

print("El arreglo antes de ordenarlo:")
print(numeros)

size = len(numeros)
quicksort(numeros, 0, size - 1)

print("\nEl arreglo después de ordenarlo:")

print(numeros)