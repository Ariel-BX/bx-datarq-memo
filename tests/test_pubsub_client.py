import pytest
from unittest.mock import patch, MagicMock
from google.oauth2 import service_account
import json
from src.infrastructure.messaging.pubsub_client import PubSubClient

@pytest.fixture
def service_account_info():
    return json.dumps({
        "type": "service_account",
        "project_id": "test-project",
        "private_key_id": "some-key-id",
        "private_key": "some-private-key",
        "client_email": "test@test-project.iam.gserviceaccount.com",
        "client_id": "some-client-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/test%40test-project.iam.gserviceaccount.com"
    })

@patch('google.oauth2.service_account.Credentials.from_service_account_info')
@patch('google.cloud.pubsub_v1.PublisherClient')
def test_get_client(mock_publisher_client, mock_credentials, service_account_info):
    mock_credentials.return_value = MagicMock(spec=service_account.Credentials)
    mock_publisher_client.return_value = MagicMock()

    pubsub_client = PubSubClient(service_account_info)
    client = pubsub_client.get_client()

    mock_credentials.assert_called_once_with(json.loads(service_account_info))
    mock_publisher_client.assert_called_once_with(credentials=mock_credentials.return_value)
    assert client == mock_publisher_client.return_value

def test_get_client_no_service_account():
    pubsub_client = PubSubClient(None)
    with pytest.raises(ValueError, match="Service Account not configured."):
        pubsub_client.get_client()