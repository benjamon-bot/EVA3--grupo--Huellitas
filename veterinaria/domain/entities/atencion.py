from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from .detalle_atencion import DetalleAtencion

ESTADOS_ATENCION = (
    "AGENDADA",
    "REALIZADA",
    "PAGADA",
    "CANCELADA",
)

TRANSICIONES_ATENCION = {
    "AGENDADA": ("REALIZADA", "CANCELADA"),
    "REALIZADA": ("PAGADA",),
    "PAGADA": (),
    "CANCELADA": (),
}


@dataclass
class Atencion:
    mascota_id: int
    motivo: str
    detalles: List[DetalleAtencion] = field(default_factory=list)
    diagnostico: Optional[str] = None
    estado: str = "AGENDADA"
    total: Decimal = Decimal("0.00")
    fecha: Optional[datetime] = None
    id: Optional[int] = None

    def calcular_total(self) -> Decimal:
        return sum(
            (detalle.subtotal for detalle in self.detalles),
            Decimal("0.00"),
        )

    def recalcular_total(self) -> None:
        self.total = self.calcular_total()

    def puede_pasar_a(self, nuevo_estado: str) -> bool:
        return nuevo_estado in TRANSICIONES_ATENCION[self.estado]

