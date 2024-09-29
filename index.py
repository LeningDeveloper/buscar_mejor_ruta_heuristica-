import heapq

# Base de conocimiento que define las conexiones entre estaciones y las distancias entre ellas.
# Cada tupla en la `base_conocimiento` representa una conexión entre estaciones con su respectiva distancia.
base_conocimiento = [
    ("A", "B", 2),
    ("A", "C", 5),
    ("A", "D", 8),
    ("B", "C", 2),
    ("B", "D", 7),
    ("C", "D", 1),
    ("C", "E", 4),
    ("D", "E", 3),
    ("D", "F", 6),
    ("E", "F", 2),
    ("F", "G", 6),
    ("G", "H", 4),
    ("H", "G", 4),
    ("H", "I", 5),
    ("I", "H", 5),
    ("I", "J", 2),
    ("J", "I", 2),
    ("J", "K", 8),
    ("K", "J", 8),
    ("B", "E", 3),  # Nueva conexión para ofrecer una ruta alternativa
    ("C", "F", 7),  # Nueva conexión para mejorar la flexibilidad de rutas
    ("E", "H", 8)   # Conexión directa que podría evitar rutas largas
]

# Heurística: función que estima la distancia restante desde un nodo hasta el destino.
def heuristica(nodo, objetivo):
    heuristica_simple = {
        'A': 10,
        'B': 9,
        'C': 8,
        'D': 7,
        'E': 6,
        'F': 5,
        'G': 4,
        'H': 3,
        'I': 2,
        'J': 1,
        'K': 0  # El destino tiene distancia 0
    }
    return heuristica_simple.get(nodo, float('inf'))  # Devuelve la estimación o infinito si el nodo no está definido

# Función para obtener los vecinos de un nodo (una estación) según la base de conocimiento.
def obtener_vecinos(base_conocimiento, nodo):
    vecinos = []
    for origen, destino, costo in base_conocimiento:
        if origen == nodo:
            vecinos.append((destino, costo))
    return vecinos

# Implementación del algoritmo A* utilizando la heurística para guiar la búsqueda.
def buscar_mejor_ruta_heuristica(base_conocimiento, inicio, objetivo):
    # Cola de prioridad para explorar los nodos en orden de prioridad (menor costo + heurística)
    open_list = []
    heapq.heappush(open_list, (0, inicio))  # Añadimos el nodo inicial con un costo de 0
    
    # Diccionarios para almacenar el costo mínimo hasta el momento y el camino más corto
    costo_actual = {inicio: 0}
    camino = {inicio: None}  # Para reconstruir la ruta una vez encontrado el objetivo
    
    while open_list:
        _, nodo_actual = heapq.heappop(open_list)  # Sacamos el nodo con menor prioridad (menor costo estimado)
        
        if nodo_actual == objetivo:
            # Si llegamos al objetivo, reconstruimos la ruta
            ruta = []
            while nodo_actual is not None:
                ruta.append(nodo_actual)
                nodo_actual = camino[nodo_actual]
            return ruta[::-1], costo_actual[objetivo]  # Devolvemos la ruta en orden correcto (inicio -> objetivo) y el costo total
        
        # Obtenemos los vecinos del nodo actual
        vecinos = obtener_vecinos(base_conocimiento, nodo_actual)
        
        for vecino, costo in vecinos:
            # Calculamos el nuevo costo para llegar al vecino desde el nodo actual
            nuevo_costo = costo_actual[nodo_actual] + costo
            # Si encontramos un camino más corto o el vecino no ha sido visitado, actualizamos el costo
            if vecino not in costo_actual or nuevo_costo < costo_actual[vecino]:
                costo_actual[vecino] = nuevo_costo
                prioridad = nuevo_costo + heuristica(vecino, objetivo)  # Función heurística aplicada aquí
                heapq.heappush(open_list, (prioridad, vecino))
                camino[vecino] = nodo_actual  # Guardamos de dónde vino para reconstruir la ruta
    
    # Si no encontramos ninguna ruta al objetivo
    return None, None

# Función para imprimir todas las estaciones disponibles y sus conexiones
def imprimir_estaciones_y_conexiones(base_conocimiento):
    print("Estaciones disponibles y sus conexiones con costos:")
    conexiones_mostradas = set()
    for origen, destino, costo in base_conocimiento:
        if (origen, destino) not in conexiones_mostradas:
            print(f"Estación {origen} -> Estación {destino} (Costo: {costo})")
            # Añadir ambas direcciones para evitar imprimir duplicados (en caso de ser bidireccional)
            conexiones_mostradas.add((origen, destino))
            conexiones_mostradas.add((destino, origen))
    print()  # Línea en blanco para separar

# Mostrar las estaciones y sus conexiones
imprimir_estaciones_y_conexiones(base_conocimiento)

# Interacción con el usuario para seleccionar estaciones
inicio = input("Ingrese la estación de inicio: ").upper()
objetivo = input("Ingrese la estación de destino: ").upper()

# Validar si las estaciones existen en la base de conocimiento
estaciones_validas = {origen for origen, _, _ in base_conocimiento} | {destino for _, destino, _ in base_conocimiento}

if inicio not in estaciones_validas or objetivo not in estaciones_validas:
    print("Estación no válida. Por favor, ingrese estaciones correctas.")
else:
    mejor_ruta, costo_total = buscar_mejor_ruta_heuristica(base_conocimiento, inicio, objetivo)
    if mejor_ruta:
        print(f"La mejor ruta desde {inicio} hasta {objetivo} es: {' -> '.join(mejor_ruta)} con un costo de {costo_total}")
    else:
        print(f"No se encontró una ruta desde {inicio} hasta {objetivo}.")
