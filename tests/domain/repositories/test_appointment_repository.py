from unittest.mock import MagicMock

import pytest

from src.domain.entities.appointment_entity import AppointmentEntity
from src.domain.repositories.appointment_repository import AppointmentRepository


def test_appointment_repository_has_save_method():
    assert hasattr(AppointmentRepository, "save")
    assert callable(getattr(AppointmentRepository, "save"))


def test_appointment_repository_has_find_by_doctor_and_availability_ids_method():
    assert hasattr(AppointmentRepository, "find_by_doctor_and_availability_ids")
    assert callable(getattr(AppointmentRepository, "find_by_doctor_and_availability_ids"))


def test_appointment_repository_has_find_by_id_method():
    assert hasattr(AppointmentRepository, "find_by_id")
    assert callable(getattr(AppointmentRepository, "find_by_id"))

# def test_appointment_repository_save_raises_not_implemented_error():
#     with pytest.raises(NotImplementedError):
#         AppointmentRepository().save(MagicMock(spec=AppointmentEntity))







