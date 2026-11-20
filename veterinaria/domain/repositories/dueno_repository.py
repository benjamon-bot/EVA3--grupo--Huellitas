from abc import ABC, abstractmethod 
from typing import List, Optional 
from veterinaria.domain.entities.dueno import Dueno 
 
 
class DuenoRepository(ABC): 
    @abstractmethod 
    def listar(self) -> List[Dueno]: ... 
 
    @abstractmethod 
    def obtener_por_rut(self, rut: str) -> Optional[Dueno]: ... 
 
    @abstractmethod 
    def existe_rut(self, rut: str) -> bool: ... 
 
    @abstractmethod 
    def existe_email(self, email: str, excluir_rut: Optional[str] = None) -> bool: ... 
 
    @abstractmethod 
    def tiene_mascotas(self, rut: str) -> bool: ... 
 
    @abstractmethod 
    def guardar(self, dueno: Dueno) -> Dueno: ... 
 
    @abstractmethod 
    def eliminar(self, rut: str) -> bool: ... 