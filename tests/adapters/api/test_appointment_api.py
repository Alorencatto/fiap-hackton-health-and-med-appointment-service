from datetime import datetime
import unittest
from unittest.mock import AsyncMock,MagicMock, patch

import pytest
from fastapi import HTTPException
from src.application.dto.appointment_dto import AppointmentCreate
from src.domain.exceptions import EntityAlreadyExists, EntityNotFound
from src.application.services.appointment_service import AppointmentService
from src.domain.entities.appointment_entity import AppointmentEntity, AppointmentStatus


#
from src.adapters.api.appointment_api import (
    create_appointment,
    update_appointment,
    read_appointment
)


class TestAppointmentAPI(unittest.IsolatedAsyncioTestCase):

    @patch("src.adapters.api.appointment_api.get_appointment_service")
    async def test_read_appointment_found(self,mock_appointment_service):

        # Arrange
        mock_service = MagicMock(spec=AppointmentService)
        mock_appointment_service.return_value = mock_service

        booking_time : datetime = datetime.now()

        appointment_entity =  AppointmentEntity(
            doctor_id=1,
            patient_id=1,
            availability_id=1,
            booking_time=booking_time,
            status=AppointmentStatus.PENDING,
            id=1
        )

        mock_service.get_appointment_by_id.return_value = appointment_entity

        # Act
        result = await read_appointment(1,mock_service)

        # Assert
        mock_service.get_appointment_by_id.assert_called_once_with(1)
        self.assertEqual(result.id, appointment_entity.id)

    @patch("src.adapters.api.appointment_api.get_appointment_service")
    async def test_read_appointment_not_found(self,mock_appointment_service):

        # Arrange
        mock_service = MagicMock(spec=AppointmentService)
        mock_appointment_service.return_value = mock_service

        mock_service.get_appointment_by_id.side_effect = EntityNotFound()

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await read_appointment(1, mock_service)

        self.assertEqual(context.exception.status_code, 404)

    @patch("src.adapters.api.appointment_api.get_appointment_service")
    async def test_create_appointment(self, mock_appointment_service):

        # Arrange
        mock_service = MagicMock(spec=AppointmentService)
        mock_appointment_service.return_value = mock_service

        appointment_create = AppointmentCreate(
            doctor_id=1,
            patient_id=1,
            availability_id=1,
        )

        booking_time : datetime = datetime.now()

        mock_service.create_appointment.return_value = AppointmentEntity(
            doctor_id=1,
            patient_id=1,
            availability_id=1,
            booking_time=booking_time,
            status=AppointmentStatus.PENDING,
            id=1
        )

        # Act
        result = await create_appointment(appointment_create, mock_service)

        # Assert
        mock_service.create_appointment.assert_called_once()
        self.assertEqual(result.id, 1)
        self.assertEqual(result.doctor_id, appointment_create.doctor_id)
        self.assertEqual(result.availability_id, appointment_create.availability_id)

    @patch("src.adapters.api.appointment_api.get_appointment_service")
    async def test_create_appointment_with_doctor_already_allocated_on_scheduling_id(self, mock_appointment_service):

        # Arrange
        mock_service = MagicMock(spec=AppointmentService)
        mock_appointment_service.return_value = mock_service

        appointment_create = AppointmentCreate(
            doctor_id=1,
            patient_id=1,
            availability_id=1,
        )

        mock_service.create_appointment.side_effect = EntityAlreadyExists()

     
        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await create_appointment(appointment_create, mock_service)

        self.assertEqual(context.exception.status_code, 400)

    @patch("src.adapters.api.appointment_api.get_appointment_service")
    async def test_update_status_for_existing_appointment(self, mock_appointment_service):
       
        # Arrange
        mock_service = MagicMock(spec=AppointmentService)
        mock_appointment_service.return_value = mock_service

        appointment_id : int = 1
        booking_time : datetime = datetime.now()
        status_update  = AppointmentStatus.CONFIRMED

        mock_service.update_appointment_status.return_value = AppointmentEntity(
            doctor_id=1,
            patient_id=1,
            availability_id=1,
            booking_time=booking_time,
            status=AppointmentStatus.CONFIRMED,
            id=1
        )

        # Act
        result = await update_appointment(appointment_id,status_update, mock_service)

        # Assert
        mock_service.update_appointment_status.assert_called_once()
        self.assertEqual(result.status,status_update.value)


    @patch("src.adapters.api.appointment_api.get_appointment_service")
    async def test_update_non_status_for_existing_appointment(self, mock_appointment_service):

       pass

    @patch("src.adapters.api.appointment_api.get_appointment_service")
    async def test_update_status_for_non_existing_appointment(self, mock_appointment_service):

       pass
       

