from db.connection_db import connect_db


QUERY_AÑO_CONSTRUCCION = " AND year = {}"
QUERY_CIUDAD = " AND city = '{}'"
QUERY_ESTADO = """WHERE status.id = '{}'
                AND status_history.update_date = (
                SELECT MAX(update_date)
                FROM status_history
                WHERE property_id = property.id
                )"""

QUERY_NOT_ESTADO = """WHERE status_history.update_date = (
                   SELECT MAX(update_date)
                   FROM status_history
                   WHERE property_id = property.id
                   )"""
ALLOWED_STATES = [3, 4, 5]


def search_response(request_data):

    """
    Crea una query SQL a partir de un JSON recibido de una petición
    POST recibida.

    Args:
        request_data (dict): Diccionario que continue los paŕametros
        de búsqueda ingresados por el usuario.

    Returns:
        data(List): LIsta de diccionarios que contienen los resultados
        de la query enviada a la base de datos

    Raises:
        TypeError: Si se genera una query no válida
    """
    try:
        inmueble_id = request_data.get('inmueble_id', 0)
        anio_construccion = request_data.get('anio_construccion', '')
        estado = request_data.get('estado', '')
        ciudad = request_data.get('ciudad', 0)
        if inmueble_id:
            query = """SELECT address, city, price, description,
                    status.name estado
                    FROM property
                    JOIN status_history ON property.id =
                    status_history.property_id
                    JOIN status ON status_history.status_id = status.id
                    WHERE property.id = '{}'
                    AND status_history.update_date = (
                    SELECT MAX(update_date)
                    FROM status_history
                    WHERE property_id = property.id
                    )"""
            query = query.format(inmueble_id)
        else:
            query = """SELECT address, city, price, description,
                    status.name estado
                    FROM property
                    JOIN status_history ON property.id =
                    status_history.property_id
                    JOIN status ON status_history.status_id = status.id
            """

            if estado and estado in ALLOWED_STATES:
                query += QUERY_ESTADO.format(estado)
            elif estado and estado not in ALLOWED_STATES:
                return {}
            else:
                query += QUERY_NOT_ESTADO.format(estado)

            if anio_construccion:
                query += QUERY_AÑO_CONSTRUCCION.format(anio_construccion)
            if ciudad:
                query += QUERY_CIUDAD.format(ciudad)
        query += """AND status.id IN (3, 4, 5)
                 AND price != 0 AND description IS NOT NULL AND name IS
                 NOT NULL AND address IS NOT NULL"""
        query += "\nGROUP BY property.id"
    except Exception:
        error_msg = ('Error: No fue obtener resultados de la consulta')
        response = {'error': error_msg}
        return response

    get_data, cursor = send_query(query)
    column_names = [des[0] for des in cursor.description]
    data = fetch_query_result(get_data, column_names)

    return data


def fetch_query_result(get_data, column_names):
    """
    Crea una lista de diccionarios, donde cada diccionario
    contiene por llave el nombre de la columna y por valor el
    contenido del campo

    Args:
        get_data (list): Lista de tuplas que los resultados
                         obtenidos de la consulta a la base de datos
        column_names(list): Lista que contiene los nombres de las columnas
        obtenidas en la ocnsulta a la base de datos

    Returns:
        data(List): LIsta de diccionarios que contienen los resultados
        de la query enviada a la base de datos
    """
    data = []
    for row in get_data:
        get_row = {column_names[i]: row[i] for i in range(len(column_names))}
        data.append(get_row)
    return data


def send_query(query):

    """
    Lanza una consulta a la base de datos y retorna el resultado y
    el cursor creado.

    Args:
        query (str): Query a enviar a la base de datos.

    Returns:
        tuple: Retorna una tupla que contiene el resultado de la consulta (get_data)
               y el cursor creado
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query)
    get_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return get_data, cursor
