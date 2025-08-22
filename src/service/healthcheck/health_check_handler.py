import os
from http.server import BaseHTTPRequestHandler

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == os.environ.get('URL_LIVENESS'):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.end_headers()
    # Evita los logs de requests en el output
    def log_message(self, format, *args):
        """
        Description: metodo que permite no mostrar los log de healthcheck
        Returns:
            None.
        """
        pass