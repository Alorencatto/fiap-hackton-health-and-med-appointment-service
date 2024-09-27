import logging
from typing import List, Optional, Tuple
import boto3
import os

import aiohttp
from fastapi import HTTPException  # TODO remove this from service
from src.infrastructure.messaging.appointment_update_publisher import AppointmentUpdatePublisher
from src.config import Config
from src.domain.entities.customer_entity import CustomerEntity
from src.domain.entities.order_entity import OrderEntity, OrderStatus
from src.domain.entities.order_item_entity import OrderItemEntity

#
from src.domain.entities.appointment_entity import AppointmentEntity, AppointmentStatus

from src.domain.exceptions import (
    EntityAlreadyExists,
    EntityNotFound,
    InvalidEntity,
)
from src.domain.repositories.customer_repository import CustomerRepository
from src.domain.repositories.order_repository import OrderRepository
from src.infrastructure.messaging.inventory_publisher import InventoryPublisher
from src.infrastructure.messaging.order_update_publisher import (
    OrderUpdatePublisher,
)

from src.domain.repositories.appointment_repository import AppointmentRepository

logger = logging.getLogger("app")

class AppointmentService:

    def __init__(
        self,
        appointment_repository: AppointmentRepository,
        appointment_publisher: AppointmentUpdatePublisher,  # TODO this should be a port
    ):
        self.appointment_repository = appointment_repository
        self.appointment_publisher = appointment_publisher

    async def create_appointment(
            self,
            appointment : AppointmentEntity
    ) -> AppointmentEntity:
        
        logger.info(f"Creating appointment for doctor {appointment.doctor_id}")

        #
        existing_appointment = self.appointment_repository.find_by_doctor_and_availability_ids(
            doctor_id=appointment.doctor_id,
            availability_id=appointment.availability_id
        )

        if existing_appointment:
            raise EntityAlreadyExists(
                f"Doctor {appointment.doctor_id} is already allocated on this availability slot"
            )

        #
        self.appointment_repository.save(appointment)

        return appointment

    async def update_appointment_status(
        self, appointment_id: int, status: AppointmentStatus
    ) -> AppointmentEntity:
        appointment : AppointmentEntity = self.appointment_repository.find_by_id(appointment_id)

        if not appointment:
            raise EntityNotFound(f"Appointment with ID '{appointment_id}' not found")
        
        #
        appointment.status = status
        
        #
        self.appointment_repository.save(appointment)

        # Publish appointment status update
        self.appointment_publisher.publish_appointment_update(
            appointment_id=appointment.id,
            status=appointment.status.value
        )

        return appointment
    
    async def get_appointment_by_id(self, appointment_id: int) -> AppointmentEntity:
        appointment = self.appointment_repository.find_by_id(appointment_id)
        if not appointment:
            raise EntityNotFound(f"Appointment with ID '{appointment_id}' not found")
     
        return appointment
    

    #
    async def notify_appointment_status_change_to_doctor_by_email(
        appointment_id : int,
        doctor_id : int,
        status : str
    ) -> None:
        
        SES_SENDER_EMAIL : str = os.getenv("SES_SENDER_EMAIL")
        
        # TODO : Recuperar esses dados com chamadas externas
        doctor_name : str = ""
        patient_name : str = ""
        scheduling_date : str = ""
        scheduling_hour : str = ""

        to_email : str = ""


        # TODO : Montar e-mail
        body : str = f"""
        Olá, Dr. {doctor_name}!
        Você tem uma nova consulta marcada!
        Paciente: {patient_name}.
        Data e horário: {scheduling_date} às {scheduling_hour}.
        """

        subject : str = "Health&Med - Nova consulta agendada"

        # TODO : Fazer integração com o AWS SES
        ses_client = boto3.client(
            'ses',
            # region_name=AWS_REGION,
            # aws_access_key_id=AWS_ACCESS_KEY_ID,
            # aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        response = ses_client.send_email(
            Source=SES_SENDER_EMAIL,
            Destination={
                'ToAddresses': [to_email],
            },
            Message={
                'Subject': {
                    'Data': subject,
                },
                'Body': {
                    'Text': {
                        'Data': body,
                    }
                }
            }
        )
        return response


        
 

