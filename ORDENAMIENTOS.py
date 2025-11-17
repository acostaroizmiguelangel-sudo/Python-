import random
import time
import matplotlib.pyplot as plt
import numpy as np
import sys
import operator

def generate_random_array(size):
    return [random.randint(0, size * 5) for _ in range(size)]

def generate_sorted_array(size):
    return list(range(size))

def generate_reverse_sorted_array(size):
    return list(range(size - 1, -1, -1))

def generate_semi_sorted_array(size, num_swaps=None):
    arr = list(range(size))
    if num_swaps is None:
        num_swaps = size // 10
    if size > 0:
        for _ in range(num_swaps):
            idx1, idx2 = random.sample(range(size), 2)
            arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
    return arr

def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]; i += 1
            else:
                arr[k] = R[j]; j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]; i += 1; k += 1
        while j < len(R):
            arr[k] = R[j]; j += 1; k += 1
    return arr

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def quick_sort(arr):
    def _quick_sort(items, low, high):
        if low < high:
            pi = partition(items, low, high)
            _quick_sort(items, low, pi - 1)
            _quick_sort(items, pi + 1, high)

    def partition(items, low, high):
        pivot = items[high]
        i = low - 1
        for j in range(low, high):
            if items[j] <= pivot:
                i += 1
                items[i], items[j] = items[j], items[i]
        items[i + 1], items[high] = items[high], items[i + 1]
        return i + 1

    _quick_sort(arr, 0, len(arr) - 1)
    return arr

def heap_sort(arr):
    def heapify(arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and arr[largest] < arr[l]:
            largest = l

        if r < n and arr[largest] < arr[r]:
            largest = r

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr

def radix_sort(arr):
    def counting_sort_for_radix(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = arr[i] // exp
            count[index % 10] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = arr[i] // exp
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1
            i -= 1

        for i in range(n):
            arr[i] = output[i]

    if not arr: 
        return arr
        
    max1 = max(arr)
    if max1 < 0:
        print("    ¡AVISO! Radix Sort no maneja negativos, saltando.")
        return arr

    exp = 1
    while max1 // exp > 0:
        counting_sort_for_radix(arr, exp)
        exp *= 10
    return arr

def bucket_sort(arr):
    if not arr:
        return arr

    max_val = max(arr)
    min_val = min(arr)

    if max_val == min_val:
        return arr

    num_buckets = len(arr)
    buckets = [[] for _ in range(num_buckets)]

    range_buckets = (max_val - min_val) + 1
    
    for num in arr:
        idx = int((num - min_val) * num_buckets / range_buckets)
        
        if idx >= num_buckets:
            idx = num_buckets - 1
            
        buckets[idx].append(num)

    idx = 0
    for bucket in buckets:
        insertion_sort(bucket) 
        for item in bucket:
            arr[idx] = item
            idx += 1
    return arr

def hash_sort(arr):
    if not arr:
        return arr
    
    counts = {}
    for x in arr:
        counts[x] = counts.get(x, 0) + 1
    
    sorted_keys = sorted(counts.keys())
    
    idx = 0
    for key in sorted_keys:
        for _ in range(counts[key]):
            arr[idx] = key
            idx += 1
    return arr

def measure_time(sort_algorithm, arr):
    arr_copy = list(arr)
    start_time = time.perf_counter()
    try:
        sort_algorithm(arr_copy)
    except RecursionError:
        print(f"    ¡ERROR! {sort_algorithm.__name__} alcanzó el límite de recursión.")
        return float('inf')
    except Exception as e:
        print(f"    ¡ERROR! {sort_algorithm.__name__} falló: {e}")
        return float('inf')
        
    end_time = time.perf_counter()
    return (end_time - start_time) * 1000

def get_verdict(algo_name, arr_type, arr_size):
    """
    Da una explicación de por qué un algoritmo es bueno o malo
    en una situación específica (versión más casual).
    """
    verdicts = {
        "Bubble Sort": "Es lentísimo. Compara a cada rato a sus vecinos. Es fácil de entender, pero la verdad, casi siempre es el peor.",
        "Selection Sort": "También es muy lento. Es terco: siempre busca el más chiquito una y otra vez, no le importa si ya estaba ordenado.",
        "Insertion Sort": "Es rápido para listas chicas o que ya estaban 'casi' listas. Pero si le das una lista al revés, se atora y se vuelve súper lento.",
        "Merge Sort": "Este es muy confiable. Siempre va a una buena velocidad sin importar qué tan revuelta esté la lista. Eso sí, pide más memoria.",
        "Quick Sort": "Casi siempre es el más veloz de todos cuando la lista está bien revuelta. Pero ten cuidado: si le das una lista ya ordenada o al revés, 'truena' y se vuelve lentísimo.",
        "Heap Sort": "Otro que es muy confiable, como el Merge Sort. Siempre va a buena velocidad y lo mejor es que no necesita memoria extra.",
        "Radix Sort": "¡Este vuela! Pero tiene truco: solo funciona bien con números. No compara, ordena por dígitos. Es como magia para listas de puros números.",
        "Bucket Sort": "Es rapidísimo si los números están bien repartidos (como en una lista aleatoria). Si todos los números son muy parecidos, se vuelve lento.",
        "Hash Sort": "Es veloz si no hay muchos números repetidos. Básicamente cuenta cuántos hay de cada uno y luego los pone en orden. Parecido al Bucket."
    }

    
    if arr_type == "Ordenado" and algo_name == "Insertion Sort":
        return "¡GANADOR OBVIO! Como la lista ya estaba ordenada, este solo le da una pasada para checar y termina. Es el más listo para este caso."
    
    if arr_type == "Ordenado" and algo_name == "Quick Sort":
        return "¡SE ATORÓ! Este es el peor escenario para Quick Sort. Cuando la lista ya está ordenada, se vuelve tonto, lentísimo y hasta puede fallar."
    
    if arr_type == "Inverso" and algo_name == "Insertion Sort":
        return "¡SU PESADILLA! Para este algoritmo, una lista al revés es lo peor. Tiene que mover CADA número a su lugar, uno por uno. LENTÍSIMO."
    
    if arr_type == "Aleatorio" and algo_name in ["Radix Sort", "Bucket Sort"]:
        return "¡EL MÁS TRAMPOSO! Para números al azar, los que no comparan (como Radix o Bucket) casi siempre ganan. Van a otro ritmo."
    
    
    return verdicts.get(algo_name, "Pues... no tengo un chisme específico para este. Hizo su trabajo.")


def plot_single_test(results_dict, arr_type, arr_size):
    sorted_results = sorted(results_dict.items(), key=lambda item: item[1])
    
    algos = [item[0] for item in sorted_results]
    times = [item[1] for item in sorted_results]
    
    plt.figure(figsize=(10, 6))
    
    colors = ['#4CAF50'] + ['#42A5F5'] * (len(algos) - 1)
    
    bars = plt.bar(algos, times, color=colors)
    
    plt.xlabel('Algoritmo de Ordenamiento')
    plt.ylabel('Tiempo de Ejecución (milisegundos)')
    plt.title(f'Comparativa: Arreglo {arr_type} de {arr_size} elementos')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    
    for bar in bars:
        yval = bar.get_height()
        if yval == float('inf'):
            plt.text(bar.get_x() + bar.get_width()/2.0, 1, 'FALLÓ', ha='center', va='bottom', color='red', weight='bold')
        else:
            plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.3f} ms', ha='center', va='bottom')
            
    print("\nMostrando gráfico en una ventana emergente...")
    plt.show()

def main():
    all_algorithms = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
        "Selection Sort": selection_sort,
        "Quick Sort": quick_sort,
        "Heap Sort": heap_sort,
        "Radix Sort": radix_sort,
        "Bucket Sort": bucket_sort,
        "Hash Sort": hash_sort,
    }
    
    all_array_types = {
        "1": ("Aleatorio", generate_random_array),
        "2": ("Ordenado", generate_sorted_array),
        "3": ("Inverso", generate_reverse_sorted_array),
        "4": ("Semi-ordenado", generate_semi_sorted_array),
    }

    all_array_sizes = {
        "1": ("100", 100),
        "2": ("1,000", 1000),
        "3": ("10,000", 10000),
        "4": ("100,000", 100000),
    }

    while True:
        print("\n--- Visualizador Interactivo de Algoritmos de Ordenamiento ---")
        
        print("Elige el 'Pre-Orden' (tipo) del arreglo:")
        for key, (name, _) in all_array_types.items():
            print(f"  [{key}] {name}")
        arr_type_choice = input("Opción (1-4): ")
        
        if arr_type_choice not in all_array_types:
            print("¡Opción inválida! Intenta de nuevo.")
            continue
            
        arr_type_name, arr_generator_func = all_array_types[arr_type_choice]

        print("\nElige el tamaño del arreglo:")
        for key, (name, _) in all_array_sizes.items():
            print(f"  [{key}] {name} elementos")
        arr_size_choice = input("Opción (1-4): ")

        if arr_size_choice not in all_array_sizes:
            print("¡Opción inválida! Intenta de nuevo.")
            continue
        
        arr_size_name, arr_size_val = all_array_sizes[arr_size_choice]

        print(f"\nEjecutando pruebas para: {arr_type_name} de {arr_size_name} elementos...")
        
        algos_to_run = all_algorithms.copy()
        if arr_size_val >= 100000:
            print(" (Omitiendo Bubble Sort y Selection Sort por ser demasiado lentos para este tamaño)")
            algos_to_run.pop("Bubble Sort", None)
            algos_to_run.pop("Selection Sort", None)

        base_array = arr_generator_func(arr_size_val)
        
        current_results = {}

        for algo_name, algo_func in algos_to_run.items():
            print(f"  Probando {algo_name}...")
            time_taken = measure_time(algo_func, base_array)
            current_results[algo_name] = time_taken

        print("\n--- Resultados y Veredicto ---")
        
        valid_results = {k: v for k, v in current_results.items() if v != float('inf')}
        
        if not valid_results:
            print("¡Todos los algoritmos fallaron para este escenario!")
            continue

        ganador_nombre, ganador_tiempo = min(valid_results.items(), key=lambda item: item[1])
        
        sorted_final_results = sorted(valid_results.items(), key=lambda item: item[1])
        
        print(f"\nResultados para {arr_type_name} de {arr_size_name} elementos:")
        for i, (algo, tiempo) in enumerate(sorted_final_results):
            print(f"  {i+1}. {algo}: {tiempo:.4f} ms")

        for algo, tiempo in current_results.items():
            if tiempo == float('inf'):
                print(f"  -. {algo}: FALLÓ (Límite de recursión o error)")
        
        print("\n--- Veredicto del Ganador ---")
        print(f"🥇 El ganador es: **{ganador_nombre}**")
        print(f"¿Por qué? {get_verdict(ganador_nombre, arr_type_name, arr_size_val)}")

        plot_single_test(current_results, arr_type_name, arr_size_name)

        continuar = input("\n¿Quieres probar otra combinación? (s/n): ")
        if continuar.lower() != 's':
            print("¡Adiós!")
            break

if __name__ == "__main__":
    main()