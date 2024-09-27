from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from src.domain.exceptions import InvalidOperation
from src.adapters.dependencies import get_appointment_service
from src.application.dto.customer_dto import CustomerCreate, CustomerResponse
from src.application.dto.serializers import serialize_customer,serialize_appointment

# dto
from src.application.dto.appointment_dto import AppointmentCreate, AppointmentResponse

# entity
from src.domain.entities.appointment_entity import AppointmentEntity,AppointmentStatus

#
# from src.infrastructure.persistence.models import AppointmentStatus as AppointmentStatusModel

from src.application.services.order_service import OrderService
from src.domain.entities.customer_entity import CustomerEntity
from src.domain.exceptions import EntityAlreadyExists, EntityNotFound

from src.application.services.appointment_service import AppointmentService



router = APIRouter()

@router.post(
    # "/availabilies/", tags=["availability"], response_model=List[CustomerResponse]
    "/appointment",
    tags=["appointment"],
    response_model=AppointmentResponse
)
async def create_appointment(
    appointment : AppointmentCreate,
    service : AppointmentService = Depends(get_appointment_service)
):
    try:
        appointment_entity = AppointmentEntity(
            doctor_id=appointment.doctor_id,
            patient_id=appointment.patient_id,
            availability_id=appointment.availability_id,
            booking_time=datetime.now(),
            status=AppointmentStatus.PENDING 
        )

        created_appointment = await service.create_appointment(
            appointment=appointment_entity
        )

        return serialize_appointment(created_appointment)

    except EntityAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))

    
@router.put(
    "/appointment/{appointment_id}/status",
    tags=["appointment"],
    response_model=AppointmentResponse
)
async def update_appointment(
    appointment_id : int,
    status_update : AppointmentStatus,
    service : AppointmentService = Depends(get_appointment_service)
):
    try:
        updated_appointment = await service.update_appointment_status(
            appointment_id=appointment_id,
            status=status_update
        )

        return serialize_appointment(updated_appointment)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidOperation as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/appointments/{appointment_id}",
    tags=["appointment"],
    response_model=AppointmentResponse
)
async def read_appointment(
    appointment_id : int,
    service : AppointmentService = Depends(get_appointment_service)
):
    try:
        appointment = await service.get_appointment_by_id(appointment_id)

        return serialize_appointment(appointment)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

