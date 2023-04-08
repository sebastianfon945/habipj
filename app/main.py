# from api.post_endpoints import handle_post_request
from http.server import HTTPServer, BaseHTTPRequestHandler
from api.post_endpoints import search_response
import json
# from about import AboutHandler


class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    """Clase para gestionar las peticiones que ingresan al servidor.

    Esta clase contiene un método do_POST desde donde se ejecutan las
    consultas a la base de datos

    Attributes:
        No tiene atributos públicos.

    Methods:
        do_POST(): Maneja una solicitud POST. Procesa los datos recibidos
        en formato JSON y retorna una respuesta HTTP.
        Gestiona las peticiones POST. recibe y envía datos en formato JSON.
        La respuesta contiene el resulta de la consulta
        a la base de datos o un posible mensaje de error.
    """

    routes = {
        '/search': search_response
    }

    def do_POST(self):
        """Gestiona las peticiones POST.

        Verifica los datos recibidos y entrega los resultados de la consulta
        a la base de datos en formato JSON.

        Verifica si la petición POST recibida contiene los datos mínimos para
        ejecutar la consulta a la base de datos.

        Ejemplo de estructura JSON esperada:

        {
            "user": "user@user.co",
            "inmueble_id": null,
            "anio_construccion": "",
            "ciudad": "bogota",
            "estado": 4
        }

        Un JSON válido para esta petición al menos uno de los siguientes
        parámetros deben ser válidos:
        "inmueble_id", "anio_construccion", "ciudad", "estado"

        Returns:
            Respuesta HTTP a la petición en formato JSON
        """
        if self.path in self.routes:
            if callable(self.routes[self.path]):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                if data:
                    check_body = [key for key, value in data.items() if value]
                    if len(check_body) == 1 and check_body[0] == 'user':
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        error_msg = ('Error: Debe ingresar al menos '
                                     'un parámetro de búsqueda')
                        response = {'error': error_msg}
                        self.wfile.write(json.dumps(response).encode('utf-8'))
                    else:
                        self.send_response(200)
                        response_content = self.routes[self.path](data)
                        json_data = json.dumps(response_content)
                        self.wfile.write(json_data.encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(self.routes[self.path], 'utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('404 Not Found', 'utf-8'))


if __name__ == '__main__':
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)
    print("Starting server...")
    httpd.serve_forever()
