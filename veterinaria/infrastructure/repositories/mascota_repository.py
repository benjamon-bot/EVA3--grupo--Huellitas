from typing import List, Optional
from veterinaria.domain.entities.mascota import Mascota
from veterinaria.domain.repositories.mascota_repository import MascotaRepository
from veterinaria.infrastructure.models.mascota import MascotaModel

CAMPOS = ["dueno_id", "nombre", "especie", "raza",
          "fecha_nacimiento", "sexo", "activo"]

def _to_entity(m):
    return Mascota(id=m.id, rut_dueno=m.dueno_id, nombre=m.nombre,
        especie=m.especie, raza=m.raza,
        fecha_nacimiento=m.fecha_nacimiento, sexo=m.sexo, activo=m.activo)

class DjangoMascotaRepository(MascotaRepository):
    def listar(self) -> List[Mascota]:
        return [_to_entity(m) for m in MascotaModel.objects.order_by("nombre")]
    def obtener_por_id(self, mascota_id) -> Optional[Mascota]:
        m = MascotaModel.objects.filter(id=mascota_id).first()
        return _to_entity(m) if m else None
    def tiene_atenciones(self, mascota_id):
        from veterinaria.infrastructure.models.atencion import AtencionModel
        return AtencionModel.objects.filter(mascota_id=mascota_id).exists()
    def guardar(self, mascota):
        valores = {"dueno_id": mascota.rut_dueno, "nombre": mascota.nombre,
            "especie": mascota.especie, "raza": mascota.raza,
            "fecha_nacimiento": mascota.fecha_nacimiento,
            "sexo": mascota.sexo, "activo": mascota.activo}
        if mascota.id is None:
            m = MascotaModel.objects.create(**valores)
        else:
            m = MascotaModel.objects.get(id=mascota.id)
            for campo, valor in valores.items(): setattr(m, campo, valor)
            m.save(update_fields=CAMPOS)
        return _to_entity(m)
    def eliminar(self, mascota_id):
        borrados, _ = MascotaModel.objects.filter(id=mascota_id).delete()
        return borrados > 0
