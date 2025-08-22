import pytest
from unittest.mock import patch, MagicMock
import json
from src.infrastructure.messaging.gcp_publisher import GCPPublisher

@pytest.fixture
def logger_service_mock():
    return MagicMock()

@pytest.fixture
def pubsub_client_mock():
    return MagicMock()

@pytest.fixture
def gcp_publisher(logger_service_mock, pubsub_client_mock):
    return GCPPublisher(pubsub_client_mock, 'test-project', 'test-topic', logger_service_mock)

@patch('google.cloud.pubsub_v1.PublisherClient')
def test_publish(mock_publisher_client, gcp_publisher, pubsub_client_mock, logger_service_mock):
    mock_client = MagicMock()
    mock_publisher_client.return_value = mock_client
    pubsub_client_mock.get_client.return_value = mock_client
    mock_client.topic_path.return_value = 'test-topic-path'
    mock_future = MagicMock()
    mock_future.result.return_value = 'message-id'
    mock_client.publish.return_value = mock_future

    message = json.dumps({
        "Message": "Test message",
        "MessageAttributes": {
            "attribute1": {"Value": "value1"},
            "attribute2": {"Value": "value2"}
        }
    })

    gcp_publisher.publish(message)

    mock_client.topic_path.assert_called_once_with('test-project', 'test-topic')
    mock_client.publish.assert_called_once_with(
        'test-topic-path', 
        b'Test message',
        attribute1="value1",
        attribute2="value2"
    )
    logger_service_mock.log.assert_called_once_with(
        message="Message sent: message-id",
        context={
            "message": "Test message",
            "messageAttributes": {
                "attribute1": "value1",
                "attribute2": "value2"
            }
        }
    )

@patch('google.cloud.pubsub_v1.PublisherClient')
def test_publish_exception(mock_publisher_client, gcp_publisher, pubsub_client_mock, logger_service_mock):
    mock_client = MagicMock()
    mock_publisher_client.return_value = mock_client
    pubsub_client_mock.get_client.return_value = mock_client
    mock_client.topic_path.return_value = 'test-topic-path'
    mock_client.publish.side_effect = Exception("Test exception")

    message = json.dumps({
        "Message": "Test message",
        "MessageAttributes": {
            "attribute1": {"Value": "value1"},
            "attribute2": {"Value": "value2"}
        }
    })

    gcp_publisher.publish(message)

    mock_client.topic_path.assert_called_once_with('test-project', 'test-topic')
    mock_client.publish.assert_called_once_with(
        'test-topic-path', 
        b'Test message',
        attribute1="value1",
        attribute2="value2"
    )
    logger_service_mock.log.assert_called_once_with(
        message="Error sending message: Test exception",
        error_type="gcp"
    )

def test_extract_message_attributes(gcp_publisher):
    message_attributes = {
        "attribute1": {"Value": "value1"},
        "attribute2": {"Value": "value2"}
    }
    result = gcp_publisher.extract_message_attributes(message_attributes)
    assert result == {
        "attribute1": "value1",
        "attribute2": "value2"
    }