import json
from datetime import datetime, timedelta
from geopy.distance import geodesic  # Para calcular la distancia entre dos puntos geográficos (coordenadas)
from sklearn.cluster import KMeans   # Algoritmo de clustering K-means para agrupar clientes cercanos
import numpy as np

# Función para cargar el archivo JSON con la información de los clientes
def cargar_rutas(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['clientes']

# Función para calcular la distancia en kilómetros entre dos clientes usando sus coordenadas
def calcular_distancia(cliente1, cliente2):
    coordenadas_cliente1 = (cliente1['latitud'], cliente1['longitud'])  # Latitud y longitud del cliente 1
    coordenadas_cliente2 = (cliente2['latitud'], cliente2['longitud'])  # Latitud y longitud del cliente 2
    return geodesic(coordenadas_cliente1, coordenadas_cliente2).kilometers  # Distancia entre ambos en km

# Función para convertir una hora (en formato de cadena "HH:MM") a un objeto datetime
def convertir_hora(hora_str):
    return datetime.strptime(hora_str, "%H:%M")

# Función para verificar si la hora actual está dentro de la ventana de tiempo de un cliente
def esta_en_ventana_tiempo(hora_actual, cliente):
    ventana_inicio = convertir_hora(cliente['ventana_tiempo']['inicio'])  # Hora de inicio de la ventana del cliente
    ventana_fin = convertir_hora(cliente['ventana_tiempo']['fin'])        # Hora de fin de la ventana del cliente
    return ventana_inicio <= hora_actual <= ventana_fin  # Devuelve True si la hora actual está dentro de la ventana

# Función para encontrar la primera hora disponible a partir de las ventanas de tiempo de todos los clientes
def encontrar_hora_inicio(clientes):
    # Busca la hora de inicio más temprana entre todas las ventanas de tiempo de los clientes
    primera_hora = min([convertir_hora(cliente['ventana_tiempo']['inicio']) for cliente in clientes])
    return primera_hora

# Función para planificar la ruta óptima dentro de un grupo de clientes
def planificar_ruta(clientes):
    ruta = []  # Lista para almacenar el orden de los clientes en la ruta
    hora_actual = encontrar_hora_inicio(clientes)  # La hora inicial es la primera ventana de tiempo disponible
    cliente_actual = None  # Inicialmente no hay un cliente actual
    
    while clientes:
        siguiente_cliente = None
        menor_distancia = float('inf')  # Inicialmente, ninguna distancia ha sido calculada
        
        # Iterar sobre los clientes para encontrar al siguiente que se puede visitar
        for cliente in clientes:
            if cliente_actual is None:
                # Si es el primer cliente, simplemente selecciona el primero cuya ventana de tiempo permita ser atendido
                if esta_en_ventana_tiempo(hora_actual, cliente):
                    siguiente_cliente = cliente
                    break
            else:
                # Si ya hay un cliente actual, busca el siguiente cliente que esté más cerca
                distancia = calcular_distancia(cliente_actual, cliente)  # Calcula la distancia entre los clientes
                tiempo_viaje = timedelta(minutes=int(distancia))  # Convertimos la distancia a minutos (1 km = 1 min)
                hora_llegada = hora_actual + tiempo_viaje  # Calcula la hora de llegada al siguiente cliente
                
                # Verifica si el siguiente cliente puede ser atendido dentro de su ventana de tiempo
                if hora_llegada <= convertir_hora(cliente['ventana_tiempo']['fin']) and distancia < menor_distancia:
                    menor_distancia = distancia  # Actualiza la menor distancia encontrada
                    siguiente_cliente = cliente  # Guarda el cliente más cercano
        
        # Si no se puede visitar ningún cliente más, termina la ruta
        if siguiente_cliente is None:
            print("No hay más clientes que puedan visitarse en la ventana de tiempo actual.")
            break
        
        # Añadir el cliente visitado a la ruta
        ruta.append(siguiente_cliente['nombre'])
        clientes.remove(siguiente_cliente)  # Remueve el cliente de la lista, ya que ha sido visitado
        cliente_actual = siguiente_cliente  # Actualiza el cliente actual
        
        # Actualiza la hora actual añadiendo el tiempo de viaje al siguiente cliente
        if menor_distancia == float('inf'):  # Si es el primer cliente, no se añade tiempo de viaje
            menor_distancia = 0
        hora_actual += timedelta(minutes=int(menor_distancia))  # Añade el tiempo de viaje a la hora actual

    return ruta  # Devuelve la ruta planificada

# Función para agrupar los clientes por cercanía usando K-means clustering
def agrupar_clientes_por_cercania(clientes, num_grupos=2):
    # Extrae las coordenadas (latitud y longitud) de los clientes
    coordenadas = np.array([(cliente['latitud'], cliente['longitud']) for cliente in clientes])
    
    # Aplica el algoritmo K-means para dividir los clientes en "num_grupos" grupos
    kmeans = KMeans(n_clusters=num_grupos)
    etiquetas = kmeans.fit_predict(coordenadas)  # Genera etiquetas para cada cliente basado en el grupo asignado
    
    # Crea un diccionario que almacenará los clientes agrupados por su etiqueta (grupo)
    grupos = {i: [] for i in range(num_grupos)}
    
    # Asigna los clientes a sus respectivos grupos según la etiqueta de K-means
    for etiqueta, cliente in zip(etiquetas, clientes):
        grupos[etiqueta].append(cliente)
    
    return grupos  # Devuelve los grupos de clientes

# Cargar los clientes desde el archivo JSON
clientes = cargar_rutas('./rutas.json')

# Agrupar los clientes en dos rutas según su cercanía
grupos_clientes = agrupar_clientes_por_cercania(clientes, num_grupos=2)

# Planificar las rutas para cada grupo
rutas = []
for grupo, clientes_grupo in grupos_clientes.items():
    print(f"\nPlanificando ruta para el grupo {grupo + 1}:")
    ruta_optima = planificar_ruta(clientes_grupo)  # Genera la ruta óptima para cada grupo de clientes
    rutas.append(ruta_optima)  # Añade la ruta generada a la lista de rutas
    print(f"La ruta más óptima para el grupo {grupo + 1} es: {ruta_optima}")
