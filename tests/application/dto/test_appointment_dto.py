from datetime import datetime
from unittest.mock import patch

import pytest
from pydantic import ValidationError
from src.domain.entities.appointment_entity import AppointmentStatus
from src.application.dto.customer_dto import CustomerCreate, CustomerResponse
from src.application.dto.appointment_dto import AppointmentCreate,AppointmentStatusUpdate,AppointmentResponse


def test_appointment_create_valid():
    appointment_data = {
        "doctor_id": 1,
        "patient_id": 1,
        "availability_id": 1
    }
    appointment = AppointmentCreate(**appointment_data)

    assert appointment.doctor_id == appointment_data["doctor_id"]
    assert appointment.patient_id == appointment_data["patient_id"]
    assert appointment.availability_id == appointment_data["availability_id"]


def test_appointment_response_valid():

    booking_time : datetime = datetime.now()

    appointment_data = {
        "doctor_id": 1,
        "patient_id": 1,
        "availability_id": 1,
        "booking_time": booking_time,
        "status" : AppointmentStatus.PENDING,
        "id":1
    }
    appointment = AppointmentResponse(**appointment_data)

    assert appointment.doctor_id == appointment_data["doctor_id"]
    assert appointment.patient_id == appointment_data["patient_id"]
    assert appointment.availability_id == appointment_data["availability_id"]
    assert appointment.booking_time == appointment_data["booking_time"]
    assert appointment.status == appointment_data["status"]




