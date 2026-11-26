from abc import ABC, abstractmethod
from typing import List

from veterinaria.domain.entities.detalle_atencion import DetalleAtencion


class DetalleAtencionRepository(ABC):
    @abstractmethod
    def listar_por_atencion(
        self, atencion_id: int
    ) -> List[DetalleAtencion]: ...

    @abstractmethod
    def guardar(
        self, detalle: DetalleAtencion
    ) -> DetalleAtencion: ...

    @abstractmethod
    def eliminar_por_atencion(self, atencion_id: int) -> int: ...

    @abstractmethod
    def servicio_esta_en_uso(self, servicio_id: int) -> bool: ...
