import asyncio
import json
import logging

import pika
from src.infrastructure.messaging.base import BaseMessagingAdapter

logger = logging.getLogger("app")


class DoctorNotificationSubscriber(BaseMessagingAdapter):
    def __init__(
        self,
        appointment_service,
        connection_params,
        max_retries=5,
        delay=5
    ):
        super().__init__(connection_params, max_retries, delay)
        self.appointment_service = appointment_service

    def start_consuming(self):
        self.channel.exchange_declare(
            exchange="appointment_exchange", exchange_type="topic", durable=True
        )
        self.channel.queue_declare(queue="appointments_queue", durable=True)
        self.channel.queue_bind(
            exchange="appointment_exchange",
            queue="appointments_queue",
            routing_key="appointments_queue",
        )

        self.channel.basic_consume(
            queue="appointments_queue",
            on_message_callback=self.on_message,
            auto_ack=False,
        )
        logger.info("Starting to consume messages from appointments_queue.")
        self.channel.start_consuming()

    def on_message(self, ch, method, properties, body):
        logger.info(f"Received message from appointments_queue: {body}")
        try:
            data = json.loads(body.decode("utf-8"))
            appointment_id = data.get("appointment_id")
            status = data.get("status")

            # TODO
            # Call to action
            print(data)

            # asyncio.run(self.appointment_service.)

            # if status == "completed":
            #     asyncio.run(self.order_service.set_paid_order(order_id))
            #     logger.info(f"Order ID {order_id} marked as paid.")
            # if status in ["refunded", "canceled"]:
            #     asyncio.run(self.order_service.cancel_order(order_id))
            #     logger.info(f"Order ID {order_id} marked as canceled.")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)
