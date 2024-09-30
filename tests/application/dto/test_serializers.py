from datetime import datetime
from unittest.mock import MagicMock

import pytest
from src.domain.entities.appointment_entity import AppointmentEntity, AppointmentStatus

from src.application.dto.serializers import (
    serialize_appointment
)

#
from src.application.dto.appointment_dto import AppointmentCreate,AppointmentStatusUpdate,AppointmentResponse


def test_serialize_appointment():

    booking_time : datetime = datetime.now()

    appointment = MagicMock(spec=AppointmentEntity)
    appointment.doctor_id = 1
    appointment.patient_id = 1
    appointment.availability_id = 1
    appointment.booking_time = booking_time
    appointment.status = AppointmentStatus.PENDING

    serialized_appointment = serialize_appointment(appointment)

    assert isinstance(serialized_appointment, AppointmentResponse)

    assert serialized_appointment.doctor_id == 1
    assert serialized_appointment.patient_id == 1
    assert serialized_appointment.availability_id == 1
    assert serialized_appointment.booking_time == booking_time
    assert serialized_appointment.status == AppointmentStatus.PENDING

 