from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.order_entity import OrderEntity
from src.domain.entities.appointment_entity import AppointmentEntity


class AppointmentRepository(ABC):

    @abstractmethod
    def save(self, appointment: AppointmentEntity):
        raise NotImplementedError

    @abstractmethod
    def find_by_doctor_and_availability_ids(
        self,
        doctor_id : int,
        availability_id : int
    ):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, appointment_id: int) -> Optional[AppointmentEntity]:
        raise NotImplementedError
