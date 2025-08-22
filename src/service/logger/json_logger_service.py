import uuid
import logging
from src.service.logger.json_logger_formatter import JsonFormatter
from src.config.config_service import ConfigService

# Clase para manejar logs
class LoggerService:
    def __init__(self):
        # Nivel de log por defecto
        self.level = ConfigService.log_level
        # Crear un logger
        self.logger = logging.getLogger()
        # Establecer el nivel de log del logger usando getattr para obtener el nivel a partir de un string
        self.logger.setLevel(getattr(logging, self.level.upper()))
        # Crear un manejador de logs para la salida a la consola
        self.handler = logging.StreamHandler()
        # Crear un formateador de logs usando la clase JsonFormatter
        self.formatter = JsonFormatter()
        # Configurar el formateador para el manejador
        self.handler.setFormatter(self.formatter)
        # Agregar el manejador al logger
        self.logger.addHandler(self.handler)

    def log(self, message, error_type=None, context=None, transaction_id=None):
        # Establecer el nivel de log para este registro
        self.level = ConfigService.log_level
        error_types = ConfigService.error_types
        error_types_list = error_types.split(',')
        if error_type in error_types_list:
            error_type_log = error_type
            self.level = 'error'
        if error_type not in error_types_list:
            error_type_log = 'undefined'
            self.level = 'info'
        
        # Crear un diccionario error_types si error_type no es None
        extra = {'error_type': error_type_log} if error_type else {}
        
        # Agregar el contexto al diccionario extra si está presente
        if context:
            extra['context'] = context
        
        # Agregar transacion_id al diccionario extra si está presente
        if transaction_id:
            extra['transaction_id'] = transaction_id
        
        # Registrar el mensaje usando el nivel correspondiente obtenido dinámicamente
        self.logger.log(getattr(logging, self.level.upper()), message, extra=extra)