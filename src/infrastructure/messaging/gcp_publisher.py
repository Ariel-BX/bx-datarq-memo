import json

class GCPPublisher:
    def __init__(self, pubsub_client, project_id, topic_id, logger_service):
        self.pubsub_client = pubsub_client
        self.project_id = project_id
        self.topic_id = topic_id
        self.logger_service = logger_service

    def publish(self, message):
        try:
            client = self.pubsub_client.get_client()
            topic_path = client.topic_path(self.project_id, self.topic_id)
            message_sqs = json.loads(message)
            aws_message_attributes = message_sqs['MessageAttributes']
            message_attributes = self.extract_message_attributes(aws_message_attributes)
            message_data = message_sqs['Message']
            future = client.publish(topic_path, message_data.encode('utf-8'), **message_attributes)
            self.logger_service.log(
                message=f"Message sent: {future.result()}",
                context={
                    "message": message_data,
                    "messageAttributes": message_attributes,
                }
            )
        except Exception as e:
            self.logger_service.log(message=f"Error sending message: {e}", error_type="gcp")

    def extract_message_attributes(self, message_attributes):
        pubsub_attributes = {}
        for key, value in message_attributes.items():
            pubsub_attributes[key] = value["Value"]
        return pubsub_attributes
