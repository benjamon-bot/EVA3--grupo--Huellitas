from dataclasses import dataclass
from datetime import date
from typing import Optional

ESPECIES = ("PERRO", "GATO", "AVE", "CONEJO", "OTRO")
SEXOS = ("MACHO", "HEMBRA")

@dataclass
class Mascota:
    rut_dueno: str
    nombre: str
    especie: str
    raza: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    sexo: Optional[str] = None
    activo: bool = True
    id: Optional[int] = None
