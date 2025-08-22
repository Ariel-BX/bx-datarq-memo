import pytest
from unittest.mock import MagicMock, patch

from src.application.messages_processors import MessagesProcessor  # Ajusta esto por la ruta de tu módulo

@pytest.fixture
def logger_service_mock():
    return MagicMock()

@patch('src.application.messages_processors.SQSConsumer')
@patch('src.application.messages_processors.GCPPublisher')
def test_start_consuming_messages(mock_gcp_publisher, mock_sqs_consumer, logger_service_mock):
    # Configuración del mock de SQSConsumer
    mock_sqs = mock_sqs_consumer.return_value
    mock_sqs.start_consuming.return_value = [('message', 'receipt_handle')]

    # Configuración del mock de GCPPublisher
    mock_gcp = mock_gcp_publisher.return_value

    # Inicializar MessagesProcessor
    message_processor = MessagesProcessor(logger_service_mock)

    # Llamar al método start_consuming_messages
    message_processor.start_consuming_messages()

    # Verificar que el mecanismo de consumación fue llamado con el argumento wait_time_seconds
    mock_sqs.start_consuming.assert_called_once_with()
    mock_sqs.delete_messages_sqs.assert_called_once_with('receipt_handle')
    mock_gcp.publish.assert_called_once_with('message')
    logger_service_mock.log.assert_called_once_with(message="Message received", context={"message": 'message'})


@patch('src.application.messages_processors.SQSConsumer')
def test_start_consuming_messages_no_messages(mock_sqs_consumer, logger_service_mock):
    # Configurar el mock para que start_consuming devuelva None
    mock_sqs_instance = mock_sqs_consumer.return_value
    mock_sqs_instance.start_consuming.return_value = None

    # Inicializar la clase
    message_processor = MessagesProcessor(logger_service=logger_service_mock)

    # Ejecutar la función
    message_processor.start_consuming_messages()

    # Verificar que se llamó a start_consuming con el argumento wait_time_seconds
    mock_sqs_instance.start_consuming.assert_called_once_with()
    mock_sqs_instance.delete_messages_sqs.assert_not_called()
    logger_service_mock.log.assert_called_once_with(message='No messages received')

@patch('src.application.messages_processors.SQSConsumer')
def test_start_consuming_messages_exception(mock_sqs_consumer, logger_service_mock):
    # Configurar el mock para que start_consuming lance una excepción
    mock_sqs_instance = mock_sqs_consumer.return_value
    mock_sqs_instance.start_consuming.side_effect = Exception("SQS Error")

    # Inicializar la clase
    messages_processor = MessagesProcessor(logger_service=logger_service_mock)
    
    # Ejecutar la función
    messages_processor.start_consuming_messages()

    # Verificar que se registró el error
    logger_service_mock.log.assert_called_once_with(
        message="Error start_consuming_messages: SQS Error",
        error_type="sqs"
    )

@patch('src.application.messages_processors.GCPPublisher')
def test_publish_message_to_gcp(mock_gcp_publisher, logger_service_mock):
    # Configuración del mock de GCPPublisher
    mock_gcp = mock_gcp_publisher.return_value

    # Inicializar MessagesProcessor
    message_processor = MessagesProcessor(logger_service_mock)

    # Llamar al método publish_message_to_gcp
    message_processor.publish_message_to_gcp('message')

    # Verificar que el mensaje fue publicado
    mock_gcp.publish.assert_called_once_with('message')

@patch('src.application.messages_processors.GCPPublisher')
def test_publish_message_to_gcp_exception(mock_gcp_publisher, logger_service_mock):
    # Configurar el mock para que publish lance una excepción
    mock_gcp_instance = mock_gcp_publisher.return_value
    mock_gcp_instance.publish.side_effect = Exception("GCP Error")

    # Inicializar la clase
    messages_processor = MessagesProcessor(logger_service=logger_service_mock)
    
    # Ejecutar la función
    messages_processor.publish_message_to_gcp('message')

    # Verificar que se registró el error
    logger_service_mock.log.assert_called_once_with(
        message="Error publishing message: GCP Error",
        error_type="gcp"
    )