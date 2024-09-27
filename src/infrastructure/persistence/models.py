import uuid

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from src.domain.entities.order_entity import OrderStatus
from src.infrastructure.persistence.db_setup import Base
import enum
from datetime import datetime
from src.domain.entities.appointment_entity import AppointmentStatus


# class AppointmentStatus(enum.Enum):
#     PENDING = "pending"
#     CONFIRMED = "confirmed"
#     CANCELLED = "cancelled"


class AppointmentModel(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)

    # doctor_id = Column(Integer, ForeignKey("doctors.id"))
    # patient_id = Column(Integer, ForeignKey("patients.id"))
    # availability_id = Column(Integer, ForeignKey("availabilities.id"))

    doctor_id = Column(Integer)
    patient_id = Column(Integer)

    availability_id = Column(Integer)
    booking_time = Column(DateTime)
    # status = Column(Enum(AppointmentStatus),nullable=False,default=AppointmentStatus.PENDING)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.PENDING)

    version = Column(Integer,nullable=False,default=0)

    # doctor = relationship("Doctor")
    # patient = relationship("Patient")
    # availability = relationship("Availability")

    created_at = Column(DateTime,default=datetime.now())
    updated_at = Column(DateTime,default=datetime.now())


# ---
class CustomerModel(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, nullable=True)
    deleted = Column(Integer, default=0)  # Logical delete column
    orders = relationship("OrderModel", back_populates="customer")


class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(
        String, unique=True, index=True, default=lambda: str(uuid.uuid4())
    )
    customer_id = Column(Integer, ForeignKey("customers.id"))
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    estimated_time = Column(String, nullable=True)
    customer = relationship("CustomerModel", back_populates="orders")
    order_items = relationship(
        "OrderItemModel", back_populates="order", cascade="all, delete-orphan"
    )


class OrderItemModel(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_sku = Column(String, index=True)
    quantity = Column(Integer)
    order = relationship("OrderModel", back_populates="order_items")
