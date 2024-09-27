from unittest.mock import MagicMock, call, patch

import pika
import pytest
from src.infrastructure.messaging.inventory_publisher import InventoryPublisher
from src.infrastructure.messaging.appointment_update_publisher import AppointmentUpdatePublisher


@patch(
    "src.infrastructure.messaging.appointment_update_publisher.BaseMessagingAdapter.__init__"
)
def test_appointment_publisher_initialization(mock_base_init):
    # Mock BaseMessagingAdapter init
    mock_base_init.return_value = None

    connection_params = MagicMock()
    publisher = AppointmentUpdatePublisher(connection_params)

    # Verify that the base class __init__ was called with the correct parameters
    mock_base_init.assert_called_once_with(connection_params, 5, 5)
    assert publisher.exchange_name == "appointment_exchange"


@patch(
    "src.infrastructure.messaging.appointment_update_publisher.BaseMessagingAdapter.connect"
)
@patch("src.infrastructure.messaging.appointment_update_publisher.logger")
@patch(
    "src.infrastructure.messaging.appointment_update_publisher.pika.BlockingConnection"
)
def test_publish_inventory_update_success(
    mock_blocking_connection, mock_logger, mock_connect
):
    mock_channel = MagicMock()
    mock_connection = MagicMock()
    mock_connection.channel.return_value = mock_channel
    mock_blocking_connection.return_value = mock_connection

    connection_params = MagicMock()
    publisher = AppointmentUpdatePublisher(connection_params)
    publisher.channel = mock_channel

    # Call the method to publish an inventory update
    publisher.publish_appointment_update(appointment_id=1, status="confirmed")

    # Verify that basic_publish was called with the correct parameters
    mock_channel.basic_publish.assert_called_once_with(
        exchange="appointment_exchange",
        routing_key="appointments_queue",
        body='{"appointment_id": 1, "status": "confirmed"}',
    )
    # mock_logger.info.assert_called_once_with(
    #     'Published appointment update: {"appointment_id": 1, "status": "confirmed"} to appointment_queue'
    # )
    mock_connect.assert_called_once()
