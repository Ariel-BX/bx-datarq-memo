from http.server import HTTPServer
from src.service.healthcheck.health_check_handler import HealthCheckHandler

def run_health_check_server():
    server_address = ('', 3000)
    httpd = HTTPServer(server_address, HealthCheckHandler)
    httpd.serve_forever()