from typing import List
from veterinaria.application.exceptions import (
    DuenoRelacionadoNoEncontradoError, EspecieInvalidaError,
    MascotaConAtencionesError, MascotaNoEncontradaError, SexoInvalidoError,
)
from veterinaria.domain.entities.mascota import ESPECIES, SEXOS, Mascota
from veterinaria.domain.repositories.dueno_repository import DuenoRepository
from veterinaria.domain.repositories.mascota_repository import MascotaRepository


def _validar(datos, duenos):
    if duenos.obtener_por_rut(datos["rut_dueno"]) is None:
        raise DuenoRelacionadoNoEncontradoError("No existe el dueño indicado.")
    if datos["especie"].upper() not in ESPECIES:
        raise EspecieInvalidaError("Especie no válida.")
    sexo = datos.get("sexo")
    if sexo and sexo.upper() not in SEXOS:
        raise SexoInvalidoError("Sexo no válido.")


class ListarMascotasUseCase:
    def __init__(self, repo): self.repo = repo
    def ejecutar(self) -> List[Mascota]: return self.repo.listar()

class ObtenerMascotaUseCase:
    def __init__(self, repo): self.repo = repo
    def ejecutar(self, mascota_id):
        mascota = self.repo.obtener_por_id(mascota_id)
        if mascota is None:
            raise MascotaNoEncontradaError(f"No existe mascota id {mascota_id}.")
        return mascota

class CrearMascotaUseCase:
    def __init__(self, repo: MascotaRepository, duenos: DuenoRepository):
        self.repo, self.duenos = repo, duenos
    def ejecutar(self, datos):
        _validar(datos, self.duenos)
        return self.repo.guardar(Mascota(
            rut_dueno=datos["rut_dueno"], nombre=datos["nombre"],
            especie=datos["especie"].upper(), raza=datos.get("raza"),
            fecha_nacimiento=datos.get("fecha_nacimiento"),
            sexo=datos["sexo"].upper() if datos.get("sexo") else None,
            activo=datos.get("activo", True)))

class ActualizarMascotaUseCase:
    def __init__(self, repo, duenos): self.repo, self.duenos = repo, duenos
    def ejecutar(self, mascota_id, datos):
        mascota = ObtenerMascotaUseCase(self.repo).ejecutar(mascota_id)
        valores = {
            "rut_dueno": datos.get("rut_dueno", mascota.rut_dueno),
            "nombre": datos.get("nombre", mascota.nombre),
            "especie": datos.get("especie", mascota.especie).upper(),
            "raza": datos.get("raza", mascota.raza),
            "fecha_nacimiento": datos.get("fecha_nacimiento", mascota.fecha_nacimiento),
            "sexo": datos.get("sexo", mascota.sexo),
            "activo": datos.get("activo", mascota.activo),
        }
        _validar(valores, self.duenos)
        mascota.rut_dueno = valores["rut_dueno"]
        mascota.nombre = valores["nombre"]
        mascota.especie = valores["especie"]
        mascota.raza = valores["raza"]
        mascota.fecha_nacimiento = valores["fecha_nacimiento"]
        mascota.sexo = valores["sexo"].upper() if valores["sexo"] else None
        mascota.activo = valores["activo"]
        return self.repo.guardar(mascota)

class EliminarMascotaUseCase:
    def __init__(self, repo): self.repo = repo
    def ejecutar(self, mascota_id):
        ObtenerMascotaUseCase(self.repo).ejecutar(mascota_id)
        if self.repo.tiene_atenciones(mascota_id):
            raise MascotaConAtencionesError(
                "No se puede eliminar una mascota con atenciones."
            )
        self.repo.eliminar(mascota_id)
