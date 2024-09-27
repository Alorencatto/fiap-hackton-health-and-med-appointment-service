from datetime import datetime
from unittest.mock import patch

import pytest
from src.domain.entities.appointment_entity import AppointmentEntity,AppointmentStatus
from src.domain.exceptions import InvalidEntity


def test_appointment_entity_initialization():
    appointment = AppointmentEntity(
        doctor_id=1,
        patient_id=1,
        availability_id=1,
        booking_time=datetime.now(),
        status=AppointmentStatus.PENDING,
        id=1
    )
    assert appointment.id == 1
    assert appointment.patient_id == 1
    assert appointment.availability_id == 1
    assert appointment.booking_time == datetime.now()


def test_appointment_entity_invalid_id():
    with pytest.raises(InvalidEntity) as exc_info:
        AppointmentEntity(
            doctor_id=1,
            patient_id=1,
            availability_id=1,
            booking_time=datetime.now(),
            status=AppointmentStatus.PENDING,
            id=-1
        )
    assert str(exc_info.value) == "ID must be a positive integer."


def test_to_dict():

    booking_time : datetime = datetime.now()

    appointment = AppointmentEntity(
        doctor_id=1,
        patient_id=1,
        availability_id=1,
        booking_time=booking_time,
        status=AppointmentStatus.PENDING,
        id=1
    )
    expected_dict = {
        "doctor_id": 1,
        "patient_id": 1,
        "availability_id": 1,
        "booking_time": booking_time,
        "status": "pending",
        "id":1
    }
    assert appointment.to_dict() == expected_dict

