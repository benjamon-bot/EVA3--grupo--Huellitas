from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

from veterinaria.domain.entities.atencion import Atencion


class AtencionRepository(ABC):
    @abstractmethod
    def listar(self) -> List[Atencion]: ...

    @abstractmethod
    def obtener_por_id(self, atencion_id: int) -> Optional[Atencion]: ...

    @abstractmethod
    def existe_agendada_en_fecha(
        self,
        mascota_id: int,
        fecha: date,
    ) -> bool: ...

    @abstractmethod
    def registrar(self, atencion: Atencion) -> Atencion: ...

    @abstractmethod
    def actualizar(self, atencion: Atencion) -> Atencion: ...

    @abstractmethod
    def cambiar_estado(
        self,
        atencion: Atencion,
        nuevo_estado: str,
    ) -> Atencion: ...

    @abstractmethod
    def eliminar(self, atencion_id: int) -> bool: ...
