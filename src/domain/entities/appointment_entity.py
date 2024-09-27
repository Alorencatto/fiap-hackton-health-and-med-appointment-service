import re
from typing import Optional
from datetime import datetime
from enum import Enum

from src.domain.exceptions import InvalidEntity


class AppointmentStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class AppointmentEntity:

    def __init__(
        self,
        doctor_id : int,
        patient_id: int,
        availability_id: int,
        booking_time : datetime,
        status : AppointmentStatus,
        version : int = 0,
        id: Optional[int] = None
    ):
        self.id = id
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.availability_id = availability_id
        self.booking_time  = booking_time
        self.status = status
        self.version = version

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: Optional[int]):
        if value is not None and value <= 0:
            raise InvalidEntity("ID must be a positive integer.")
        self._id = value

    # @property
    # def status(self) -> AppointmentStatus:
    #     return self._status

    # @status.setter
    # def status(self,value : str):
    #     try:
    #         self._status = AppointmentStatus(value)
    #     except ValueError as e:
    #         print(e)
    #         # raise InvalidEntity("Invalid appointment status.")

    # def update_status(self, new_status: AppointmentStatus):
    #     # self.status = new_status
    #     print(new_status)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "doctor_id": self.doctor_id,
            "patient_id": self.patient_id,
            "availability_id": self.availability_id,
            "booking_time": self.booking_time,
            "status" : self.status
        }
