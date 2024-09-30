from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
import pytest
import unittest

from src.application.services.order_service import OrderService
from src.domain.entities.customer_entity import CustomerEntity
from src.domain.entities.order_entity import OrderEntity, OrderStatus
from src.domain.entities.order_item_entity import OrderItemEntity
from src.domain.exceptions import (
    EntityAlreadyExists,
    EntityNotFound,
    InvalidEntity,
)
from src.infrastructure.messaging.inventory_publisher import InventoryPublisher
from src.infrastructure.messaging.order_update_publisher import (
    OrderUpdatePublisher,
)

#
from src.domain.entities.appointment_entity import AppointmentEntity, AppointmentStatus
from src.application.services.appointment_service import AppointmentService


# Creating with class method
class TestAppointmentService(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        
        # Arrange
        self.mock_appointment_repository = MagicMock()
        self.mock_appointment_publisher = MagicMock()

        self.appointment_service = AppointmentService(
            appointment_repository=self.mock_appointment_repository,
            appointment_publisher=self.mock_appointment_publisher
        )

        booking_time : datetime = datetime.now()

        self.appointment = AppointmentEntity(
            doctor_id=1,
            patient_id=1,
            availability_id=1,
            booking_time=booking_time,
            status=AppointmentStatus.PENDING
        )

    async def test_create_appointment_success(self):

        # Arrange
        self.mock_appointment_repository.find_by_doctor_and_availability_ids.return_value = None

        # Act
        appointment = await self.appointment_service.create_appointment(
            self.appointment
        )

        # Assert
        self.mock_appointment_repository.find_by_doctor_and_availability_ids.assert_called_once_with(
            doctor_id=self.appointment.doctor_id,
            availability_id=self.appointment.availability_id
        )

        self.assertEqual(appointment, self.appointment)

    async def test_create_appointment_with_doctor_already_allocated_on_scheduling_id(self):

        # Arrange
        self.mock_appointment_repository.find_by_doctor_and_availability_ids.return_value = self.appointment

        # Act & Assert
        with self.assertRaises(EntityAlreadyExists):
            await self.appointment_service.create_appointment(
                self.appointment
            )


    def test_get_appointment_by_id_not_found(self):

        # Arrange
        self.mock_appointment_repository.find_by_id.return_value = None

        # Act & Assert
        with self.assertRaises(EntityNotFound):
            self.appointment_service.get_appointment_by_id(self.appointment.id)

        # self.appointment_service.get_appointment_by_id(self.appointment.id)

    # def test_get_appointment_by_id_success(self):
    #     # Arrange
    #     self.mock_appointment_repository.find_by_id.return_value = self.appointment

    #     # Act
    #     appointment = self.appointment_service.get_appointment_by_id(self.appointment.id)

    #     # Assert
    #     self.mock_appointment_repository.find_by_id.assert_called_once_with(
    #         appointment.id
    #     )
    #     # self.assertEqual(appointment, self.appointment)
    




# def test_delete_customer(order_service, mock_customer_repository):
#     customer = CustomerEntity(
#         name="John Doe",
#         email="john.doe@example.com",
#         phone_number="+123456789",
#     )

#     mock_customer_repository.find_by_email.return_value = customer

#     order_service.delete_customer("john.doe@example.com")

#     assert mock_customer_repository.delete.called




# @pytest.mark.asyncio
# async def test_get_order_by_id_found(order_service, mock_order_repository):
#     customer = CustomerEntity(
#         id=1,
#         name="John Doe",
#         email="john@example.com",
#         phone_number="+123456789",
#     )  # Valid phone number
#     order = OrderEntity(id=1, customer=customer, order_items=[])
#     mock_order_repository.find_by_id.return_value = order

#     result = await order_service.get_order_by_id(1)

#     mock_order_repository.find_by_id.assert_called_once_with(1)
#     assert result == order


# @pytest.mark.asyncio
# async def test_get_order_by_id_not_found(order_service, mock_order_repository):
#     mock_order_repository.find_by_id.return_value = None

#     with pytest.raises(EntityNotFound):
#         await order_service.get_order_by_id(1)

#     mock_order_repository.find_by_id.assert_called_once_with(1)


# @pytest.mark.asyncio
# async def test_update_order_status(order_service, mock_order_repository):
#     customer = CustomerEntity(
#         id=1,
#         name="John Doe",
#         email="john@example.com",
#         phone_number="+123456789",
#     )  # Valid phone number
#     order = OrderEntity(
#         id=1, customer=customer, order_items=[], status=OrderStatus.PENDING
#     )
#     mock_order_repository.find_by_id.return_value = order
#     mock_order_repository.save.return_value = order

#     result = await order_service.update_order_status(1, OrderStatus.CONFIRMED)

#     mock_order_repository.find_by_id.assert_called_once_with(1)
#     mock_order_repository.save.assert_called_once_with(order)
#     assert result.status == OrderStatus.CONFIRMED


# @pytest.mark.asyncio
# async def test_confirm_order_invalid_status(
#     order_service, mock_order_repository
# ):
#     customer = CustomerEntity(
#         id=1,
#         name="John Doe",
#         email="john@example.com",
#         phone_number="+123456789",
#     )  # Valid phone number
#     order = OrderEntity(
#         id=1, customer=customer, order_items=[], status=OrderStatus.CONFIRMED
#     )
#     mock_order_repository.find_by_id.return_value = order

#     with pytest.raises(InvalidEntity):
#         await order_service.confirm_order(1)

#     mock_order_repository.find_by_id.assert_called_once_with(1)


# @pytest.mark.asyncio
# @patch("src.application.services.order_service.aiohttp.ClientSession.get")
# async def test_cancel_order(mock_get, order_service):
#     # Mocking the external inventory service response
#     mock_get.return_value.__aenter__.return_value.status = 200
#     mock_get.return_value.__aenter__.return_value.json = AsyncMock(
#         return_value={"quantity": 10}
#     )

#     customer = CustomerEntity(
#         id=1,
#         name="John Doe",
#         email="john@example.com",
#         phone_number="+123456789",
#     )
#     order = OrderEntity(
#         id=1,
#         customer=customer,
#         order_items=[OrderItemEntity(product_sku="SKU123", quantity=2)],
#         status=OrderStatus.PENDING,
#     )

#     order_service.order_repository.find_by_id.return_value = order
#     order_service.order_repository.save.return_value = order

#     result = await order_service.cancel_order(1)

#     order_service.order_repository.find_by_id.assert_called_once_with(1)
#     order_service.order_repository.save.assert_called_once_with(order)
#     assert result.status == OrderStatus.CANCELED


# @pytest.mark.asyncio
# async def test_delete_order(order_service, mock_order_repository):
#     customer = CustomerEntity(
#         id=1,
#         name="John Doe",
#         email="john@example.com",
#         phone_number="+123456789",
#     )  # Valid phone number
#     order = OrderEntity(id=1, customer=customer, order_items=[])
#     mock_order_repository.find_by_id.return_value = order

#     result = await order_service.delete_order(1)

#     mock_order_repository.find_by_id.assert_called_once_with(1)
#     mock_order_repository.delete.assert_called_once_with(order)
#     assert result == order


# @pytest.mark.asyncio
# async def test_create_customer_success(
#     order_service, mock_customer_repository
# ):
#     customer = CustomerEntity(
#         name="Jane Doe", email="jane@example.com", phone_number="+987654321"
#     )  # Valid phone number
#     mock_customer_repository.find_by_email.return_value = None

#     result = order_service.create_customer(customer)

#     mock_customer_repository.find_by_email.assert_called_once_with(
#         customer.email
#     )
#     mock_customer_repository.save.assert_called_once_with(customer)
#     assert result == customer


# @pytest.mark.asyncio
# async def test_create_customer_already_exists(
#     order_service, mock_customer_repository
# ):
#     customer = CustomerEntity(
#         name="Jane Doe", email="jane@example.com", phone_number="+987654321"
#     )  # Valid phone number
#     existing_customer = CustomerEntity(
#         id=1,
#         name="Jane Doe",
#         email="jane@example.com",
#         phone_number="+987654321",
#     )
#     mock_customer_repository.find_by_email.return_value = existing_customer

#     with pytest.raises(EntityAlreadyExists):
#         order_service.create_customer(customer)

#     mock_customer_repository.find_by_email.assert_called_once_with(
#         customer.email
#     )
#     mock_customer_repository.save.assert_not_called()


# @pytest.mark.asyncio
# async def test_update_customer_success(
#     order_service, mock_customer_repository
# ):
#     customer = CustomerEntity(
#         name="Jane Doe", email="jane@example.com", phone_number="+987654321"
#     )  # Valid phone number
#     updated_customer = CustomerEntity(
#         name="Jane Smith",
#         email="jane.smith@example.com",
#         phone_number="+987654321",
#     )
#     mock_customer_repository.find_by_email.return_value = customer

#     result = order_service.update_customer(
#         "jane@example.com", updated_customer
#     )

#     mock_customer_repository.find_by_email.assert_called_once_with(
#         "jane@example.com"
#     )
#     mock_customer_repository.save.assert_called_once_with(customer)
#     assert customer.name == updated_customer.name
#     assert customer.email == updated_customer.email


# @pytest.mark.asyncio
# async def test_update_customer_not_found(
#     order_service, mock_customer_repository
# ):
#     updated_customer = CustomerEntity(
#         name="Jane Smith",
#         email="jane.smith@example.com",
#         phone_number="+987654321",
#     )  # Valid phone number
#     mock_customer_repository.find_by_email.return_value = None

#     with pytest.raises(EntityNotFound):
#         order_service.update_customer("jane@example.com", updated_customer)

#     mock_customer_repository.find_by_email.assert_called_once_with(
#         "jane@example.com"
#     )



# ------------------------------------------------------------------------------------------------------
# @pytest.mark.asyncio
# @patch("src.application.services.order_service.aiohttp.ClientSession.get")
# async def test_create_order_insufficient_inventory(mock_get, order_service):
#     customer = CustomerEntity(
#         name="John Doe",
#         email="john.doe@example.com",
#         phone_number="+123456789",
#     )
#     order_items = [OrderItemEntity(product_sku="SKU123", quantity=10)]

#     mock_get.return_value.__aenter__.return_value.status = 200
#     mock_get.return_value.__aenter__.return_value.json = AsyncMock(
#         return_value={"quantity": 5}
#     )

#     with pytest.raises(Exception):
#         await order_service.create_order(customer, order_items)


# @pytest.mark.asyncio
# @patch("src.application.services.order_service.aiohttp.ClientSession.get")
# async def test_update_order_insufficient_inventory(mock_get, order_service):
#     customer = CustomerEntity(
#         name="John Doe",
#         email="john.doe@example.com",
#         phone_number="+123456789",
#     )
#     order_items = [OrderItemEntity(product_sku="SKU123", quantity=10)]
#     existing_order = OrderEntity(
#         id=1, customer=customer, order_items=order_items
#     )

#     mock_get.return_value.__aenter__.return_value.status = 200
#     mock_get.return_value.__aenter__.return_value.json = AsyncMock(
#         return_value={"quantity": 5}
#     )

#     with pytest.raises(Exception):
#         await order_service.update_order(1, customer, order_items)


# @pytest.mark.asyncio
# @patch("src.application.services.order_service.aiohttp.ClientSession.get")
# async def test_calculate_order_total(mock_get, order_service):
#     customer = CustomerEntity(
#         name="John Doe",
#         email="john.doe@example.com",
#         phone_number="+123456789",
#     )
#     order_items = [OrderItemEntity(product_sku="SKU123", quantity=2)]
#     existing_order = OrderEntity(
#         id=1, customer=customer, order_items=order_items
#     )

#     mock_get.return_value.__aenter__.return_value.status = 200
#     mock_get.return_value.__aenter__.return_value.json = AsyncMock(
#         return_value={"price": 10.0}
#     )

#     total = await order_service.calculate_order_total(existing_order)

#     assert total == 20.0




