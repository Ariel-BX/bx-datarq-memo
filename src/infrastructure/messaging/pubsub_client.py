"""
import os
import json
from google.cloud import pubsub_v1
from google.oauth2 import service_account

class PubSubClient:
    def _init_(self, service_account_path_or_json: str):
        self._sa = service_account_path_or_json
        self._credentials = None
        self._client = None

    def _get_credentials(self):
        if self._credentials:
            return self._credentials

        sa = (self._sa or "").strip()

        # Si es una ruta a archivo .json
        if os.path.exists(sa):
            self._credentials = service_account.Credentials.from_service_account_file(sa)
            return self._credentials

        # Si es JSON inline
        try:
            info = json.loads(sa)
            self._credentials = service_account.Credentials.from_service_account_info(info)
            return self._credentials
        except json.JSONDecodeError:
            raise ValueError(
            )

    def get_client(self) -> pubsub_v1.PublisherClient:
        if self._client:
            return self._client
        creds = self._get_credentials()
        self._client = pubsub_v1.PublisherClient(credentials=creds)
        return self._client
"""    


from google.cloud import pubsub_v1
from google.oauth2 import service_account
import json

class PubSubClient:
    def __init__(self, service_account_info):
        self.service_account_info = service_account_info

    def get_client(self):
        if not self.service_account_info:
            raise ValueError("Service Account not configured.")
        credentials_info = json.loads(self.service_account_info)
        credentials = service_account.Credentials.from_service_account_info(credentials_info)
        return pubsub_v1.PublisherClient(credentials=credentials)
