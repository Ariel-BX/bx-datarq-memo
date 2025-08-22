import os
from dotenv import load_dotenv

load_dotenv()

class ConfigService:
    env = os.getenv("ENV", "local").upper()
    log_level = os.getenv("BX_LOG_LEVEL", "error").upper()
    error_types = os.getenv("BX_ERROR_TYPES")
    bx_queue_name = os.getenv("BX_QUEUE_NAME")
    aws_region_name = os.getenv("AWS_REGION")
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    gcp_credentials = os.getenv("GCP_CREDENTIALS")
    gcp_project_id = os.getenv("GCP_PROJECT")
    gcp_topic_id = os.getenv("GCP_TOPIC_ID")
    gcp_sa = os.getenv("GCP_SA")
    attribute_names = os.getenv("ATTRIBUTE_NAMES", "All")  # Asegurarse de que sea una cadena
    max_number_of_messages = int(os.getenv("MAX_NUMBER_OF_MESSAGES", 10))  # Asegurarse de que sea un entero
    message_attribute_names = os.getenv("MESSAGE_ATTRIBUTE_NAMES", "All")  # Asegurarse de que sea una cadena
    visibility_timeout = int(os.getenv("VISIBILITY_TIMEOUT", 30))  # Asegurarse de que sea un entero
    wait_time_seconds = int(os.getenv("WAIT_TIME_SECONDS", 20))  # Asegurarse de que sea un entero
