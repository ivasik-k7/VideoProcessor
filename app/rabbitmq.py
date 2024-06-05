import pika

from app.config import rabbitmq_config as config
from app.logger import get_logger

logger = get_logger(__name__)

TASK_TOPIC = "TASKS"


class RabbitMQService:
    def __init__(self):
        logger.info("Opening the connection to RabbitMQ Server")

        credentials = pika.PlainCredentials(
            username=config.USERNAME,
            password=config.PASSWORD,
            erase_on_connect=True,
        )

        connection_params = pika.ConnectionParameters(
            host=config.HOST,
            port=config.PORT,
            credentials=credentials,
        )

        connection = pika.BlockingConnection(connection_params)

        self.channel = connection.channel()

    def send_message(self, message, queue_name=TASK_TOPIC):
        try:
            self.channel.queue_declare(queue=queue_name)

            self.channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=message,
            )

            logger.info(f"Message sent to queue '{queue_name}': {message}")
        except Exception as e:
            logger.exception("Error sending message via RabbitMQ: ", e)

    def consume_message(self, external_callback):
        try:
            self.channel.queue_declare(queue=TASK_TOPIC)

            def callback(ch, method, properties, body):
                external_callback(body)

            self.channel.basic_consume(
                queue=TASK_TOPIC,
                on_message_callback=callback,
                auto_ack=True,
            )

            logger.info("Waiting for messages. To exit, press CTRL+C")
            self.channel.start_consuming()
        except Exception as e:
            logger.exception("Error RabbitMQ consuming messages: ", e)

    def close_connection(self):
        self.channel.close()
        logger.info("RabbitMQ connection closed.")


class RabbitMQContext:
    def __init__(self) -> None:
        self.service = RabbitMQService()

    def __enter__(self):
        return self.service

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            logger.exception("RabbitMQ error occurred: ", exc_value)
        self.server.close_connection()
