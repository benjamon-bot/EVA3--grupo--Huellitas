from typing import List, Optional
from veterinaria.domain.entities.servicio import Servicio
from veterinaria.domain.repositories.servicio_repository import ServicioRepository
from veterinaria.infrastructure.models.servicio import ServicioModel

CAMPOS = ["nombre", "descripcion", "precio", "activo"]

def _to_entity(m):
    return Servicio(id=m.id, nombre=m.nombre, descripcion=m.descripcion,
        precio=m.precio, activo=m.activo)

class DjangoServicioRepository(ServicioRepository):
    def listar(self) -> List[Servicio]:
        return [_to_entity(m) for m in ServicioModel.objects.order_by("nombre")]
    def obtener_por_id(self, servicio_id) -> Optional[Servicio]:
        m = ServicioModel.objects.filter(id=servicio_id).first()
        return _to_entity(m) if m else None
    def existe_nombre(self, nombre, excluir_id=None):
        q = ServicioModel.objects.filter(nombre=nombre)
        if excluir_id is not None: q = q.exclude(id=excluir_id)
        return q.exists()
    def esta_en_uso(self, servicio_id):
        from veterinaria.infrastructure.models.detalle_atencion import DetalleAtencionModel
        return DetalleAtencionModel.objects.filter(servicio_id=servicio_id).exists()
    def guardar(self, servicio):
        valores = {campo: getattr(servicio, campo) for campo in CAMPOS}
        if servicio.id is None:
            m = ServicioModel.objects.create(**valores)
        else:
            m = ServicioModel.objects.get(id=servicio.id)
            for campo, valor in valores.items(): setattr(m, campo, valor)
            m.save(update_fields=CAMPOS)
        return _to_entity(m)
    def eliminar(self, servicio_id):
        borrados, _ = ServicioModel.objects.filter(id=servicio_id).delete()
        return borrados > 0
