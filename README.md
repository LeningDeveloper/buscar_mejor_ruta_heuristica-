1. Crear un entorno virtual (venv)
Abre una terminal o línea de comandos y navega hasta la carpeta donde se encuentra el archivo del código.


cd ruta/donde/guardaste/el/archivo
Crea un entorno virtual ejecutando el siguiente comando:

python -m venv .venv
Activa el entorno virtual:

Windows:
.venv\Scripts\activate

source .venv/bin/activate
Verás que el prompt de la terminal cambia para indicar que estás en el entorno virtual.

2. Instalar las librerías necesarias
Ejecuta el siguiente comando para instalar todas las librerías requeridas:

pip install geopy scikit-learn numpy
Estas librerías incluyen:
geopy: Para calcular distancias entre puntos geográficos (coordenadas).
scikit-learn: Para el algoritmo K-means de agrupación de clientes.
numpy: Para trabajar con arrays y realizar cálculos numéricos.

3. Ejecutar el código
Ejecuta el archivo Python utilizando el siguiente comando en la terminal:
python nombre_del_archivo.py
