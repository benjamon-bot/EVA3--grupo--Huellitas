from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class DetalleAtencion:
    servicio_id: int
    cantidad: int
    precio_unitario: Decimal
    atencion_id: Optional[int] = None

    @property
    def subtotal(self) -> Decimal:
        return self.cantidad * self.precio_unitario
