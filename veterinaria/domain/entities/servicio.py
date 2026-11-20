from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class Servicio:
    nombre: str
    precio: Decimal
    descripcion: Optional[str] = None
    activo: bool = True
    id: Optional[int] = None
