from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import update
from src.domain.entities.customer_entity import CustomerEntity
from src.domain.entities.order_entity import OrderEntity
from src.domain.entities.order_item_entity import OrderItemEntity
from src.domain.repositories.order_repository import OrderRepository
from src.infrastructure.persistence.models import (
    CustomerModel,
    OrderItemModel,
    OrderModel,
)

#
from src.domain.entities.appointment_entity import AppointmentEntity

#
from src.domain.repositories.appointment_repository import AppointmentRepository

#
from src.infrastructure.persistence.models import AppointmentModel


class SQLAlchemyAppointmentRepository(AppointmentRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, appointment: AppointmentEntity):

        db_appointment : AppointmentModel = (
            self.db.query(AppointmentModel)
            .filter(AppointmentModel.id == appointment.id)
            .first()
        )

        appointment_model = AppointmentModel(
            doctor_id=appointment.doctor_id,
            patient_id=appointment.patient_id,
            availability_id=appointment.availability_id,
            booking_time=appointment.booking_time,
            status=appointment.status.value
        )


        if not db_appointment:
            
            self.db.add(appointment_model)
            self.db.commit()
            self.db.refresh(appointment_model)
            appointment.id = appointment_model.id

        else:
            db_appointment.doctor_id = appointment_model.doctor_id
            db_appointment.patient_id = appointment_model.patient_id
            db_appointment.availability_id = appointment_model.availability_id
            db_appointment.booking_time = appointment_model.booking_time
            db_appointment.status = appointment_model.status

            self.db.commit()

        return appointment

    def find_by_doctor_and_availability_ids(
        self,
        doctor_id : int,
        availability_id : int
    ):
        doctor_appointment = (
            self.db.query(AppointmentModel).filter(
                AppointmentModel.doctor_id == doctor_id,
                AppointmentModel.availability_id == availability_id
            )
            .first()
        )

        return doctor_appointment
    
    def find_by_id(self, appointment_id: int) -> Optional[AppointmentEntity]:
        db_appointment =  (
            self.db.query(AppointmentModel)
            .filter(AppointmentModel.id == appointment_id)
            .first()
        )

        if db_appointment:

            return AppointmentEntity(
                doctor_id=db_appointment.doctor_id,
                patient_id=db_appointment.patient_id,
                availability_id=db_appointment.availability_id,
                booking_time=db_appointment.booking_time,
                status=db_appointment.status,
                id=db_appointment.id
            )
        
        return None