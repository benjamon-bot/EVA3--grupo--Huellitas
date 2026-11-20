from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from .detalle_atencion import DetalleAtencion

TRANSICIONES = {
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
    total: Decimal = Decimal("0")
    fecha: Optional[datetime] = None
    id: Optional[int] = None

    def calcular_total(self):
        return sum((d.subtotal for d in self.detalles), Decimal("0"))

    def puede_pasar_a(self, nuevo_estado):
        return nuevo_estado in TRANSICIONES[self.estado]
