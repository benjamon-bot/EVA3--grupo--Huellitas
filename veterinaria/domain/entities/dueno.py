from dataclasses import dataclass 
from datetime import datetime 
from typing import Optional 

@dataclass 
class Dueno:
    rut: str 
    nombre: str 
    telefono: Optional[str] = None 
    email: Optional[str] = None 
    direccion: Optional[str] = None 
    fecha_registro: Optional[datetime] = None