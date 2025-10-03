def eliminar_duplicados(arr):
    resu = []
    vis = set()
    for num in arr:
        if num not in vis:
            resu.append(num)
            vis.add(num)
    return resu


entrada = [3, 5, 3, 7, 5, 9, 1, 1,2,3,]
salida = eliminar_duplicados(entrada)
print(salida)
