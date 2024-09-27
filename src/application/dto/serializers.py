from src.application.dto.customer_dto import CustomerResponse
from src.application.dto.order_dto import OrderResponse
from src.application.dto.order_item_dto import OrderItemResponse
from src.domain.entities.customer_entity import CustomerEntity
from src.domain.entities.order_entity import OrderEntity
from src.domain.entities.order_item_entity import OrderItemEntity

from src.domain.entities.appointment_entity import AppointmentEntity,AppointmentStatus
from src.application.dto.appointment_dto import AppointmentCreate, AppointmentResponse


def serialize_order(order: OrderEntity, total_amount: float) -> OrderResponse:
    return OrderResponse(
        id=order.id,
        order_number=order.order_number,
        customer=serialize_customer(order.customer),
        order_items=[serialize_order_item(item) for item in order.order_items],
        status=order.status,
        total_amount=total_amount,
        estimated_time=order.estimated_time,
    )


def serialize_order_item(order_item: OrderItemEntity) -> OrderItemResponse:
    return OrderItemResponse(
        product_sku=order_item.product_sku,
        quantity=order_item.quantity,
        name=order_item.name,
        description=order_item.description,
        price=order_item.price,
    )


def serialize_customer(customer: CustomerEntity) -> CustomerResponse:
    return CustomerResponse(
        id=customer.id,
        name=customer.name,
        email=customer.email,
        phone_number=customer.phone_number,
    )

def serialize_appointment(appointment : AppointmentEntity) -> AppointmentResponse:

    appointment_response = AppointmentResponse(
        id=appointment.id,
        doctor_id=appointment.doctor_id,
        patient_id=appointment.patient_id,
        availability_id=appointment.availability_id,
        booking_time=appointment.booking_time,
        status=appointment.status.value
    )

    # if appointment.id:
    #     appointment_response.id = appointment.id

    return appointment_response