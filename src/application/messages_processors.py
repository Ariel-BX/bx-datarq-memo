from src.infrastructure.messaging.sqs_consumer import SQSConsumer
from src.infrastructure.messaging.gcp_publisher import GCPPublisher
from src.infrastructure.messaging.pubsub_client import PubSubClient
from src.config.config_service import ConfigService


class MessagesProcessor:
    def __init__(self, logger_service):
        self.logger_service = logger_service

    def start_consuming_messages(self):
        try:
            sqs = SQSConsumer(ConfigService.bx_queue_name, self.logger_service)
            messages = sqs.start_consuming()
            if messages is not None:
                for message, receipt_handle in messages:
                    if not message.strip():
                        self.logger_service.log(message="Empty message received",context={"message": message})
                        continue
                    self.logger_service.log(message="Message received",context={"message": message})
                    self.publish_message_to_gcp(message)
                    sqs.delete_messages_sqs(receipt_handle)
            else:
                self.logger_service.log(message="No messages received")
        except Exception as e:
            self.logger_service.log(message=f"Error start_consuming_messages: {e}", error_type="sqs")

    def publish_message_to_gcp(self, message):
        try:
            pubsub_client = PubSubClient(ConfigService.gcp_sa)
            gcp_publisher = GCPPublisher(
                pubsub_client,
                ConfigService.gcp_project_id, 
                ConfigService.gcp_topic_id, 
                self.logger_service)
            gcp_publisher.publish(message)
        except Exception as e:
            self.logger_service.log(message=f"Error publishing message: {e}", error_type="gcp")
