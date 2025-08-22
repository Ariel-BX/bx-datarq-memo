import logging
import json
import os

# Clase para formatear registros de logging como JSON
class JsonFormatter(logging.Formatter):
    def format(self, record):
        # Crear un diccionario con la información del registro
        record_dict = {
            'timestamp': self.formatTime(record),  # Agregar marca de tiempo
            'level': record.levelname,  # Agregar nivel de log (INFO, WARNING, etc.)
            'aplication_id': os.environ.get('APPLICATION_ID'),  # ID de la aplicación
            'transaction_id': getattr(record, 'transaction_id', ''), #id de transacción en caso de que aplique. Si no aplica dejar en blanco en el log
            'subdomain': os.environ.get('SUBDOMAIN'),  # Subdominio asociado
            'message': record.getMessage(),  # Mensaje del registro
            'error_type': getattr(record, 'error_type', ''), #tipo de error database,dataframe u otro
            'context': getattr(record, 'context', {})
        }
        # Convertir el diccionario a una cadena JSON
        return json.dumps(record_dict)