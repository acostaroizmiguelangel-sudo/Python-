import random
import os
#primera revison 26/09/25

FILAS = 5
COLUMNAS = 5
MAR = ""
SUBMARINO = "S"
DESCTRUCTOR = "D"
DESCTRUCTOR_VERTICAL = "A"
DISPARO_FALLIDO = "-"
DISPARO_ACERTADO = "*"
DISPARO_INICIALES = 8
CANTIDAD_BARCOS_INICIALES = 8
JUGADOR_1 = "J1"
JUGADOR_2 = "J2"

def obtener_matriz_inicial():
    matriz = []
    for y in range(FILAS):
        matriz.append
        for x in range (COLUMNAS):
            matriz[y].append(MAR)
    return matriz

def imprimir_letra(letra):
    return chr(ord(letra)+1)

def imprimir_separador_horizontal():
    for _ in range (COLUMNAS+1):
        print("+--", end="")
    print("+")

def imprimir_fila_numeros():
    print("| ", end="")
    for x in range(COLUMNAS):
        print(f"| {x+1} ", end="")
    print("|")

def es_mar(x, y, matriz):
    return matriz [y][x] == MAR

def coordenada_en_rango(x, y):
    return x >= 0 and x <= COLUMNAS -1 and y >= 0 and y <= FILAS -1

def colocar_e_imprimir_barcos(matriz, cantidad_barcos, jugador):
    barcos_una_celda = cantidad_barcos //2
    barcos_dos_celdas_verticales = cantidad_barcos //4
    barcos_dos_celdas_horizontales = cantidad_barcos //4
    if jugador == JUGADOR_1:
        print("Se estan imprimiendo los barcos del jugador 1")
    else:
        print("Se estan imprimiendo los barcos del jugador 2")
    print(f"Barcos de una celda: {barcos_una_celda}\nBarcos verticales de dos celdas: {barcos_dos_celdas_verticales}\n Barcos horizontales de dos celdas: {barcos_dos_celdas_horizontales}\nTotal: {barcos_una_celda+barcos_dos_celdas_verticales+barcos_dos_celdas_horizontales}")
    matriz = colocar_barcos_de_dos_celdas_horizontal(barcos_dos_celdas_horizontales, DESCTRUCTOR, matriz)
    matriz = colocar_barcos_de_dos_celdas_verticales(barcos_dos_celdas_verticales, DESCTRUCTOR, matriz)
    matriz = colocar_barcos_de_una_celda(barcos_una_celda, SUBMARINO, matriz)
    return matriz

def obtener_x_aleatoria():
    return random.randint(0, COLUMNAS-1)

def obtener_y_aleatoria():
    return random.randint(0, FILAS-1)

def colocar_barcos_de_una_celda(cantidad, tipo_barco, matriz):
    barcos_colocados = 0
    while True:
        x = obtener_x_aleatoria
        y = obtener_y_aleatoria
        if es_mar(x, y, matriz):
            matriz[y][x] = tipo_barco
            barcos_colocados += 1
        if barcos_colocados >= cantidad:
            break
    return matriz

def colocar_barcos_de_dos_celdas_horizontal(cantidad, tipo_barco, matriz):
    barcos_colocados = 0
    while True:
        x = obtener_x_aleatoria
        y = obtener_y_aleatoria
        x2 = x+1
        if coordenada_en_rango(x, y,) and coordenada_en_rango(x2,y) and es_mar(x, y, matriz) and es_mar(x2, y, matriz):
            matriz[y][x] = tipo_barco
            matriz[y][x] = tipo_barco
            barcos_colocados += 1
        if barcos_colocados >= cantidad:
            break
    return matriz

def colocar_barcos_de_dos_celdas_verticales(cantidad, tipo_barco, matriz):
    barcos_colocados = 0
    while True:
        x = obtener_x_aleatoria
        y = obtener_y_aleatoria
        y2 = y+1
        if coordenada_en_rango(x, y,) and coordenada_en_rango(x,y2) and es_mar(x, y, matriz) and es_mar(x, y2, matriz):
            matriz[y][x] = tipo_barco
            matriz[y][x] = tipo_barco
            barcos_colocados += 1
        if barcos_colocados >= cantidad:
            break
    return matriz

def imprimir_matriz(matriz, deberia_mostrar_barcos, jugador ):
    print(f"Este es el mar del jugador {jugador}: ")
    letra = "A"
    for y in range(FILAS):
        imprimir_separador_horizontal
        print(f"| {letra} ", end="")
        for x in range(COLUMNAS):
            celda = matriz[y][x]
            valor_real =celda
            if not deberia_mostrar_barcos and valor_real != MAR and valor_real != DISPARO_FALLIDO and valor_real != DISPARO_ACERTADO:
                valor_real("|")
        imprimir_separador_horizontal
        imprimir_fila_numeros
        imprimir_separador_horizontal

def incrementar_letra(letra):
    return chr(ord(letra)+1)

def imprimir_separador_horizontal():
    for _ in range(COLUMNAS+1):
        print("+---", end="")
    print("+")

def imprimir_fila_de_numeros():
    print("| ",end="")
    for x in range(COLUMNAS):
        print(f"| {x+1} ", end="")
    print("|")
