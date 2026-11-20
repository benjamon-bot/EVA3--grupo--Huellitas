from typing import List, Optional 
from veterinaria.domain.entities.dueno import Dueno 
from veterinaria.domain.repositories.dueno_repository import DuenoRepository 
from veterinaria.infrastructure.models.dueno import DuenoModel 
 
 
def _to_entity(m): 
    return Dueno(rut=m.rut, nombre=m.nombre, telefono=m.telefono, 
                 email=m.email, direccion=m.direccion, 
                 fecha_registro=m.fecha_registro) 
 
 
class DjangoDuenoRepository(DuenoRepository): 
    def listar(self) -> List[Dueno]: 
        return [_to_entity(m) for m in DuenoModel.objects.order_by("nombre")] 
 
    def obtener_por_rut(self, rut: str) -> Optional[Dueno]: 
        m = DuenoModel.objects.filter(rut=rut).first() 
        return _to_entity(m) if m else None 
 
    def existe_rut(self, rut: str) -> bool: 
        return DuenoModel.objects.filter(rut=rut).exists() 
 
    def existe_email(self, email: str, excluir_rut=None) -> bool: 
        q = DuenoModel.objects.filter(email=email) 
        if excluir_rut is not None: 
            q = q.exclude(rut=excluir_rut) 
        return q.exists() 
 
    def tiene_mascotas(self, rut: str) -> bool: 
        # Import local mientras Joaquin integra MascotaModel. 
        from veterinaria.infrastructure.models.mascota import MascotaModel 
        return MascotaModel.objects.filter(dueno_id=rut).exists() 
 
    def guardar(self, dueno: Dueno) -> Dueno: 
        m = DuenoModel.objects.filter(rut=dueno.rut).first() 
        if m is None: 
            m = DuenoModel.objects.create( 
                rut=dueno.rut, nombre=dueno.nombre, 
                telefono=dueno.telefono, email=dueno.email, 
                direccion=dueno.direccion) 
            m.refresh_from_db() 
        else: 
            m.nombre = dueno.nombre 
            m.telefono = dueno.telefono 
            m.email = dueno.email 
            m.direccion = dueno.direccion 
            m.save(update_fields=["nombre", "telefono", "email", "direccion"]) 
        return _to_entity(m) 
 
    def eliminar(self, rut: str) -> bool: 
        borrados, _ = DuenoModel.objects.filter(rut=rut).delete() 
        return borrados > 0 