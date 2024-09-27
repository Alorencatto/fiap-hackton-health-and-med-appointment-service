import logging
import threading
from contextlib import asynccontextmanager

import pika
from fastapi import FastAPI
from src.infrastructure.messaging.doctor_notification_subscriber import DoctorNotificationSubscriber
from src.adapters.api import health_api,  appointment_api
from src.adapters.dependencies import (
    get_appointment_publisher
)

from src.infrastructure.persistence.sqlalchemy_appointment_repository import SQLAlchemyAppointmentRepository
from src.application.services.appointment_service import AppointmentService
from src.infrastructure.persistence.db_setup import SessionLocal



# Set up logging
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()

    appointment_repository = SQLAlchemyAppointmentRepository(db)
    appointment_publisher = get_appointment_publisher()

    appointment_service : AppointmentService = AppointmentService(
        appointment_repository,
        appointment_publisher
    )
    connection_params = pika.ConnectionParameters(
        host="localhost", heartbeat=120
    )

    doctor_notification_subscriber = DoctorNotificationSubscriber(
        appointment_service,
        connection_params
    )
    # threading.Thread(target=doctor_notification_subscriber.start_consuming).start()
    yield


app = FastAPI(lifespan=lifespan, root_path="/appointment")

app.include_router(health_api.router)
app.include_router(appointment_api.router)
