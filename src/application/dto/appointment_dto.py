from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from src.application.dto.customer_dto import CustomerCreate, CustomerResponse
from src.application.dto.order_item_dto import (
    OrderItemCreate,
    OrderItemResponse,
)
from src.domain.entities.order_entity import OrderStatus

from src.domain.entities.appointment_entity import AppointmentEntity,AppointmentStatus


class PaginationMeta(BaseModel):
    current_page: int
    records_per_page: int
    number_of_pages: int
    total_records: int


class AppointmentCreate(BaseModel):
    doctor_id : int
    patient_id : int
    availability_id : int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "doctor_id": 1,
                    "patient_id": 1,
                    "availability_id": 1
                },
                 {
                    "doctor_id": 2,
                    "patient_id": 2,
                    "availability_id": 2
                },
            ]
        }
    }

class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatus

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"status": "in_transit"},
                {"status": "delivered"},
            ]
        }
    }

class AppointmentResponse(BaseModel):
    doctor_id : int
    patient_id : int
    availability_id : int
    booking_time : datetime
    status : AppointmentStatus
    id : Optional[int]


# --------------------- REMOVE

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "confirmed",
                },
                {
                    "status": "paid",
                },
            ]
        }
    }


class OrderResponse(BaseModel):
    id: int
    order_number: str
    customer: CustomerResponse
    order_items: List[OrderItemResponse]
    status: OrderStatus
    total_amount: float
    estimated_time: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "order_number": "ORD123",
                    "customer": {
                        "id": 1,
                        "name": "John Doe",
                        "email": "john.doe@example.com",
                        "phone_number": "+123456789",
                    },
                    "order_items": [
                        {"product_sku": "ABC123", "quantity": 2},
                        {"product_sku": "XYZ456", "quantity": 1},
                    ],
                    "status": "confirmed",
                    "total_amount": 30.00,
                    "estimated_time": "02:30",
                }
            ]
        },
    }


class EstimatedTimeUpdate(BaseModel):
    estimated_time: str

    model_config = {
        "json_schema_extra": {"examples": [{"estimated_time": "02:30"}]}
    }


class OrdersPaginatedResponse(BaseModel):
    orders: List[OrderResponse]
    pagination: PaginationMeta

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "orders": [
                        {
                            "id": 1,
                            "order_number": "ORD123",
                            "customer": {
                                "id": 1,
                                "name": "John Doe",
                                "email": "john.doe@example.com",
                                "phone_number": "+123456789",
                            },
                            "order_items": [
                                {"product_sku": "ABC123", "quantity": 2},
                                {"product_sku": "XYZ456", "quantity": 1},
                            ],
                            "status": "confirmed",
                            "total_amount": 30.00,
                            "estimated_time": "02:30",
                        }
                    ],
                    "pagination": {
                        "current_page": 1,
                        "records_per_page": 1,
                        "number_of_pages": 5,
                        "total_records": 5,
                    },
                }
            ]
        }
    }
