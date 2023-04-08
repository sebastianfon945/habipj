Como solución a la funcionalidad de Servicio de consulta, se proponen los siguientes puntos:
* Crear un servidor usando la librería http. Crear handlers para la lectura, escritura y envío de datos a través de las peticiones enviadas desde el frontend
* La conexión a la base de datos se hace a través de la librería msql.
* La creación de las queries se hace a partir de los criterios dadados en el requerimiento.
- Los inmuebles con estados distintos a pre_venta, en_venta y vendido nunca deben ser visibles por el usuario.
- Los usuarios pueden filtrar estos inmuebles por: Año de construcción, Ciudad, Estado(enviando el id).
- Los usuarios pueden aplicar varios filtros en la misma consulta.
- Los usuarios pueden ver la siguiente información del inmueble: Dirección, Ciudad,
  Estado, Precio de venta y Descripción.
* Usar patrón de diseño de enrutamiento, donde se usa un archivo main para mapear las rutas y validaciones básicas. Mientras que para la lógica y comportamiento especifico de cada enpoint se define un archivo dentro de la ruta api.


Los puntos mencionados anteriormente se búscan gestionar a través de procesos propios de SQL, tratando de evitar la mayor cantidad de verificaciones y correcciones hechas con Python. Esto buscando la mayor eficiencia en la ejecución de las peticiones hechas al backend.

Se estandariza la respuesta del API con estructuras JSON, pensando en ofrecer facilidad al frontend en la visualización de los datos.

Para la correcta lectura de las credenciales de acceso a la base de datos se debe crear un archivo .env en la raíz del proyecto, con el siguiente formato:

HOST = "HOST"
DB_USER = "DB_USER"
PASSWORD = "PASSWORD"
DATABASE = "DATABASE"
PORT = "PORT"

O también es posible escribirlo directamente en el conector que se encuentra en el archivo connection_db.py

db_connector = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        port=PORT
    )
