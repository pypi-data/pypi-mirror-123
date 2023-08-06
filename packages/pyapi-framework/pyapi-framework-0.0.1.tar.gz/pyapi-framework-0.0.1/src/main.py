from http.server import HTTPServer
from service_handler import ServiceHandler


server = HTTPServer(('127.0.0.1', 8000), ServiceHandler)
server.serve_forever()
