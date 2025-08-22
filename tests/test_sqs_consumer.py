import pytest
from unittest.mock import MagicMock, patch
import json

from src.infrastructure.messaging.sqs_consumer import SQSConsumer  # Ajusta esto según la ruta de tu módulo

@pytest.fixture
def logger_service_mock():
    return MagicMock()

@patch('boto3.Session')
def test_sqs_consumer_initialization(mock_boto_session, logger_service_mock):
    mock_session = MagicMock()
    mock_boto_session.return_value = mock_session
    mock_sqs_client = MagicMock()
    mock_session.client.return_value = mock_sqs_client
    mock_sqs_client.get_queue_url.return_value = {'QueueUrl': 'https://sqs.us-west-2.amazonaws.com/123456789012/test-queue'}

    consumer = SQSConsumer(queue_name='test-queue', logger_service=logger_service_mock)

    assert consumer.queue_url == 'https://sqs.us-west-2.amazonaws.com/123456789012/test-queue'
    assert consumer.logger_service == logger_service_mock

@patch('boto3.Session')
def test_get_sqs_client(mock_boto_session, logger_service_mock):
    mock_session = MagicMock()
    mock_boto_session.return_value = mock_session
    mock_sqs_client = MagicMock()
    mock_session.client.return_value = mock_sqs_client

    consumer = SQSConsumer(queue_name='test-queue', logger_service=logger_service_mock)
    result = consumer.get_sqs_client()

    assert result == mock_sqs_client

@patch('boto3.Session')
def test_get_queue_url(mock_boto_session, logger_service_mock):
    mock_session = MagicMock()
    mock_boto_session.return_value = mock_session
    mock_sqs_client = MagicMock()
    mock_session.client.return_value = mock_sqs_client
    mock_sqs_client.get_queue_url.return_value = {'QueueUrl': 'https://sqs.us-west-2.amazonaws.com/123456789012/test-queue'}

    consumer = SQSConsumer(queue_name='test-queue', logger_service=logger_service_mock)
    result = consumer.get_queue_url(mock_sqs_client, 'test-queue')

    assert result == 'https://sqs.us-west-2.amazonaws.com/123456789012/test-queue'

@patch('boto3.Session')
def test_start_consuming(mock_boto_session, logger_service_mock):
    mock_session = MagicMock()
    mock_boto_session.return_value = mock_session
    mock_sqs_client = MagicMock()
    mock_session.client.return_value = mock_sqs_client
    mock_sqs_client.get_queue_url.return_value = {'QueueUrl': 'https://sqs.us-west-2.amazonaws.com/123456789012/test-queue'}
    mock_sqs_client.receive_message.return_value = {
        'Messages': [
            {'Body': '{"Message": "{\"key\": \"value\"}"}', 'ReceiptHandle': 'handle1'}
        ]
    }

    consumer = SQSConsumer(queue_name='test-queue', logger_service=logger_service_mock)
    messages = consumer.start_consuming()
    print("asdlkfjaklsdfkjalskfjkasklfjkjds")
    assert messages is not None

@patch('boto3.Session')
def test_start_consuming_exception_handle(mock_boto_session, logger_service_mock):
    mock_session = MagicMock()
    mock_boto_session.return_value = mock_session
    mock_sqs_client = MagicMock()
    mock_session.client.return_value = mock_sqs_client
    mock_sqs_client.get_queue_url.return_value = {'QueueUrl': 'https://sqs.us-west-2.amazonaws.com/123456789012/test-queue'}
    mock_sqs_client.receive_message.return_value = {
        'Messages': [
            {'Body': '{"Message": "{\"key\": \"value\"}"}'}  # Missing 'ReceiptHandle'
        ]
    }

    consumer = SQSConsumer(queue_name='test-queue', logger_service=logger_service_mock)
    messages = consumer.start_consuming()

    logger_service_mock.log.assert_called_once_with(
        message="Ocurrio un error en el procesamiento de los mensajes: 'ReceiptHandle'",
        error_type='sqs'
    )
    assert messages is None or len(messages) == 0

@patch('boto3.Session')
def test_add_attributes_to_send_gcp(mock_boto_session, logger_service_mock):
    consumer = SQSConsumer(queue_name='test-queue', logger_service=logger_service_mock)
    message_sqs = {'Message': '{"key": "value"}'}
    result = consumer.add_attributes_to_send_gcp(message_sqs)

    expected_result = json.dumps({
        "key": "value",
        "dateIngestionRow": None,
        "dateTimeMetadata": None,
        "operation": None,
        "dme_messageId": None,
        "dme_commerce": None,
        "dme_country": None,
        "dme_eventId": None
    })

    assert result == expected_result

@patch('boto3.Session')
def test_delete_messages_sqs(mock_boto_session, logger_service_mock):
    mock_session = MagicMock()
    mock_boto_session.return_value = mock_session
    mock_sqs_client = MagicMock()
    mock_session.client.return_value = mock_sqs_client
    mock_sqs_client.get_queue_url.return_value = {'QueueUrl': 'https://sqs.us-west-2.amazonaws.com/123456789012/test-queue'}

    consumer = SQSConsumer(queue_name='test-queue', logger_service=logger_service_mock)
    consumer.delete_messages_sqs('handle1')

    mock_sqs_client.delete_message.assert_called_once_with(
        QueueUrl='https://sqs.us-west-2.amazonaws.com/123456789012/test-queue',
        ReceiptHandle='handle1'
    )

@patch('boto3.Session')
def test_delete_messages_sqs_exception_handle(mock_boto_session, logger_service_mock):
    mock_session = MagicMock()
    mock_boto_session.return_value = mock_session
    mock_sqs_client = MagicMock()
    mock_session.client.return_value = mock_sqs_client
    mock_sqs_client.get_queue_url.return_value = {'QueueUrl': 'https://sqs.us-west-2.amazonaws.com/123456789012/test-queue'}
    mock_sqs_client.delete_message.side_effect = Exception("Test exception")

    consumer = SQSConsumer(queue_name='test-queue', logger_service=logger_service_mock)
    result = consumer.delete_messages_sqs('handle1')

    logger_service_mock.log.assert_called_once_with(
        message="Error deleting message: Test exception",
        error_type="sqs"
    )
    assert result is None

@patch('boto3.Session')
def test_receive_messages(mock_boto_session, logger_service_mock):
    mock_session = MagicMock()
    mock_boto_session.return_value = mock_session
    mock_sqs_client = MagicMock()
    mock_session.client.return_value = mock_sqs_client
    mock_sqs_client.get_queue_url.return_value = {'QueueUrl': 'https://sqs.us-west-2.amazonaws.com/123456789012/test-queue'}
    mock_sqs_client.receive_message.return_value = {
        'Messages': [
            {'Body': '{"key": "value"}', 'ReceiptHandle': 'handle1'}
        ]
    }

    consumer = SQSConsumer(queue_name='test-queue', logger_service=logger_service_mock)
    result = consumer.receive_messages()

    assert result is not None
    assert len(result['Messages']) == 1
    assert result['Messages'][0]['ReceiptHandle'] == 'handle1'

@patch('boto3.Session')
def test_receive_messages_exception_handle(mock_boto_session, logger_service_mock):
    mock_session = MagicMock()
    mock_boto_session.return_value = mock_session
    mock_sqs_client = MagicMock()
    mock_session.client.return_value = mock_sqs_client
    mock_sqs_client.get_queue_url.return_value = {'QueueUrl': 'https://sqs.us-west-2.amazonaws.com/123456789012/test-queue'}
    mock_sqs_client.receive_message.side_effect = Exception("Test exception")

    consumer = SQSConsumer(queue_name='test-queue', logger_service=logger_service_mock)
    result = consumer.receive_messages()

    logger_service_mock.log.assert_called_once_with(
        message="Error receiving messages: Test exception",
        error_type="sqs"
    )
    assert result is None

@patch('boto3.Session')
def test_send_message(mock_boto_session, logger_service_mock):
    mock_session = MagicMock()
    mock_boto_session.return_value = mock_session
    mock_sqs_client = MagicMock()
    mock_session.client.return_value = mock_sqs_client
    mock_sqs_client.get_queue_url.return_value = {'QueueUrl': 'https://sqs.us-west-2.amazonaws.com/123456789012/test-queue'}

    consumer = SQSConsumer(queue_name='test-queue', logger_service=logger_service_mock)
    message = {"key": "value"}
    consumer.send_message(message)

    mock_sqs_client.send_message.assert_called_once_with(
        QueueUrl='https://sqs.us-west-2.amazonaws.com/123456789012/test-queue',
        MessageBody=json.dumps(message)
    )

@patch('boto3.Session')
def test_send_message_exception_handle(mock_boto_session, logger_service_mock):
    mock_session = MagicMock()
    mock_boto_session.return_value = mock_session
    mock_sqs_client = MagicMock()
    mock_session.client.return_value = mock_sqs_client
    mock_sqs_client.get_queue_url.return_value = {'QueueUrl': 'https://sqs.us-west-2.amazonaws.com/123456789012/test-queue'}
    mock_sqs_client.send_message.side_effect = Exception("Test exception")

    consumer = SQSConsumer(queue_name='test-queue', logger_service=logger_service_mock)
    message = {"key": "value"}
    result = consumer.send_message(message)

    logger_service_mock.log.assert_called_once_with(
        message="Error sending message: Test exception",
        error_type="sqs"
    )
    assert result is None
    