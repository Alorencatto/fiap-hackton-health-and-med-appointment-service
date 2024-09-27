import json
import logging

import pika
from src.infrastructure.messaging.base import BaseMessagingAdapter

logger = logging.getLogger("app")


class AppointmentUpdatePublisher(BaseMessagingAdapter):
    def __init__(self, connection_params, max_retries=5, delay=5):
        super().__init__(connection_params, max_retries, delay)
        self.exchange_name = "appointment_exchange"

    def publish_appointment_update(self, appointment_id: int, status: str):
        message = json.dumps(
            {"appointment_id": appointment_id, "status": status}
        )
        try:
            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key="appointments_queue",
                body=message,
            )
            logging.info(f"Published appointment update: {message} to appointment_queue")
        except pika.exceptions.ConnectionClosed:
            logging.error("Connection closed, attempting to reconnect.")
            self.connect()
            self.publish_appointment_update(appointment_id, status)
