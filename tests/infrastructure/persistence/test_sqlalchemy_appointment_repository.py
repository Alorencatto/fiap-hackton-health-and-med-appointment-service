from datetime import datetime
import unittest
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.orm import Session
from src.domain.entities.customer_entity import CustomerEntity
from src.infrastructure.persistence.models import CustomerModel
from src.infrastructure.persistence.sqlalchemy_customer_repository import (
    SQLAlchemyCustomerRepository,
)

from src.domain.entities.appointment_entity import AppointmentEntity, AppointmentStatus
from src.infrastructure.persistence.models import AppointmentModel
from src.infrastructure.persistence.sqlalchemy_appointment_repository import SQLAlchemyAppointmentRepository


@pytest.fixture
def mock_session():
    return MagicMock(spec=Session)


@pytest.fixture
def appointment_repository(mock_session):
    return SQLAlchemyAppointmentRepository(db=mock_session)

def test_save_new_appointment(appointment_repository, mock_session):
    appointment = AppointmentEntity(
        doctor_id=1,
        patient_id=1,
        availability_id=1,
        booking_time=datetime.now(),
        status=AppointmentStatus.PENDING
    )

    mock_db_appointment = MagicMock(spec=AppointmentModel)
    mock_db_appointment.id = 1  # Explicitly setting the ID to an integer
    mock_session.query(AppointmentModel).filter().first.return_value = None 
    mock_session.add.return_value = None
    mock_session.refresh.return_value = None
    mock_session.refresh.side_effect = lambda x: setattr(
        x, "id", mock_db_appointment.id
    )

    appointment_repository.save(appointment)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


def test_save_existing_appointment(appointment_repository, mock_session):
    db_appointment = MagicMock(spec=AppointmentModel)
    db_appointment.id = 1  # Explicitly setting the ID to an integer
    mock_session.query(AppointmentModel).filter().first.return_value = db_appointment

    booking_time : datetime = datetime.now()

    appointment = AppointmentEntity(
        doctor_id=1,
        patient_id=1,
        availability_id=1,
        booking_time=booking_time,
        status=AppointmentStatus.PENDING
    )

    appointment_repository.save(appointment)

    assert db_appointment.doctor_id == 1
    assert db_appointment.patient_id == 1
    assert db_appointment.availability_id == 1
    assert db_appointment.booking_time == booking_time

    mock_session.commit.assert_called_once()


def test_find_by_id_existing_appointment(appointment_repository, mock_session):
    # Mocking an existing apointment in the database
    db_appointment = MagicMock(spec=AppointmentModel)
    db_appointment.id = 1
    db_appointment.patient_id = 1
    db_appointment.availability_id = 1

    mock_session.query(AppointmentModel).filter().first.return_value = db_appointment

    appointment = appointment_repository.find_by_id(1)

    assert appointment is not None
    assert appointment.id == 1
    assert appointment.patient_id == 1
    assert appointment.availability_id == 1

    mock_session.query(AppointmentModel).filter().first.assert_called_once()


def test_find_by_id_non_existing_appointment(
    appointment_repository, mock_session
):
    # Mocking a non-existing customer
    mock_session.query(AppointmentModel).filter().first.return_value = None

    appointment = appointment_repository.find_by_id(0)

    assert appointment is None
    mock_session.query(AppointmentModel).filter().first.assert_called_once()

