def inserccion(a):
    for i in range(1, len(a)):
        temp = a[i]
        j = i - 1
        while j >= 0 and temp < a[j]:
            a[j + 1] = a[j]
            j = j - 1
        a[j + 1] = temp

def printArr(a):
    for i in range(len(a)):
        print(a[i], end=" ")

a = [70, 15, 2, 51, 60]
print("Esta es la lista antes de ordenarla: ")
printArr(a)
inserccion(a)
print("\nLa lista despues de ordenarla: ")
printArr(a)
