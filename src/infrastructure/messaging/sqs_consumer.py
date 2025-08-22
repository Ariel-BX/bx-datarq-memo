import boto3
import json
from src.config.config_service import ConfigService


class SQSConsumer:
    def __init__(self, queue_name, logger_service):
        session = boto3.Session( profile_name="default") if ConfigService.env == "local"  else boto3.Session()

        self.sqs =  session.client('sqs')

        self.queue_url = self.get_queue_url(self.sqs, queue_name)
        self.logger_service = logger_service

    # Método que se encarga de obtener el cliente de SQS
    def get_sqs_client(self):
        return self.sqs

    # Método que se encarga de obtener la URL de la cola SQS
    def get_queue_url(self, sqs, queue_name):
        response = sqs.get_queue_url(QueueName=queue_name)
        return response['QueueUrl']

    # Método que se encarga de consumir los mensajes de la cola SQS
    def start_consuming(self):
        response = self.receive_messages()
        if not response or 'Messages' not in response:
            return None

        messages = []
        for message in response['Messages']:
            try:
                receipt_handle = message['ReceiptHandle']
                message_sqs = json.loads(message['Body'])
                print("="*30)
                print(message_sqs)
                message_sqs['Message'] = self.add_attributes_to_send_gcp(message_sqs)
                #messages.append((json.dumps(message_sqs), receipt_handle))
                messages.append(message_sqs, receipt_handle)
            except Exception as e:
                self.logger_service.log(
                    message=f"Ocurrio un error en el procesamiento de los mensajes: {e}",
                    error_type="sqs"
                )
        return messages
        
    def add_attributes_to_send_gcp(self, message_sqs):

        message_data = message_sqs['Message']
        
        message_data_parsed = json.loads(message_data)

        message_data2 = message_data_parsed['Message']

        message_data_parsed2 = json.loads(message_data2)
        
        message_data_parsed2['dateIngestionRow'] = None
        message_data_parsed2['dateTimeMetadata'] = None
        message_data_parsed2['operation'] = None
        message_data_parsed2["dme_messageId"] = None
        message_data_parsed2["dme_commerce"] = None
        message_data_parsed2["dme_country"] = None
        message_data_parsed2["dme_eventId"] = None

        return json.dumps(message_data_parsed2)

    # Método que se encarga de eliminar los mensajes de la cola SQS
    def delete_messages_sqs(self, receipt_handle):
        try:
            self.sqs.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle
            )
        except Exception as e:
            self.logger_service.log(message=f"Error deleting message: {e}", error_type="sqs")
            return None

    # Método que se encarga de recibir los mensajes de la cola SQS
    def receive_messages(self):
        try:
            response = self.sqs.receive_message(
            QueueUrl=self.queue_url,
            AttributeNames=[ConfigService.attribute_names],
            MaxNumberOfMessages=ConfigService.max_number_of_messages,
            MessageAttributeNames=[ConfigService.message_attribute_names],
            VisibilityTimeout=ConfigService.visibility_timeout,
            WaitTimeSeconds=ConfigService.wait_time_seconds
)
            return response
        except Exception as e:
            self.logger_service.log(message=f"Error receiving messages: {e}", error_type="sqs")
            return None

    # Método que se encarga de enviar mensajes a la cola SQS
    def send_message(self, message):
        try:
            self.sqs.send_message(
                QueueUrl=self.queue_url,
                MessageBody=json.dumps(message),
            )
        except Exception as e:
            self.logger_service.log(message=f"Error sending message: {e}", error_type="sqs")
            return None
