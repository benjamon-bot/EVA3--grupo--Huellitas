from decimal import Decimal
from typing import List
from veterinaria.application.exceptions import (
    PrecioServicioInvalidoError, ServicioDuplicadoError,
    ServicioEnUsoError, ServicioNoEncontradoError,
)
from veterinaria.domain.entities.servicio import Servicio
from veterinaria.domain.repositories.servicio_repository import ServicioRepository


def _validar_precio(precio):
    if precio < Decimal("0"):
        raise PrecioServicioInvalidoError("El precio no puede ser negativo.")

class ListarServiciosUseCase:
    def __init__(self, repo): self.repo = repo
    def ejecutar(self) -> List[Servicio]: return self.repo.listar()

class ObtenerServicioUseCase:
    def __init__(self, repo): self.repo = repo
    def ejecutar(self, servicio_id):
        servicio = self.repo.obtener_por_id(servicio_id)
        if servicio is None:
            raise ServicioNoEncontradoError(f"No existe servicio id {servicio_id}.")
        return servicio

class CrearServicioUseCase:
    def __init__(self, repo): self.repo = repo
    def ejecutar(self, datos):
        precio = Decimal(str(datos["precio"]))
        _validar_precio(precio)
        if self.repo.existe_nombre(datos["nombre"]):
            raise ServicioDuplicadoError("Ya existe un servicio con ese nombre.")
        return self.repo.guardar(Servicio(
            nombre=datos["nombre"], precio=precio,
            descripcion=datos.get("descripcion"), activo=datos.get("activo", True)))

class ActualizarServicioUseCase:
    def __init__(self, repo): self.repo = repo
    def ejecutar(self, servicio_id, datos):
        servicio = ObtenerServicioUseCase(self.repo).ejecutar(servicio_id)
        servicio.nombre = datos.get("nombre", servicio.nombre)
        servicio.descripcion = datos.get("descripcion", servicio.descripcion)
        servicio.precio = Decimal(str(datos.get("precio", servicio.precio)))
        servicio.activo = datos.get("activo", servicio.activo)
        _validar_precio(servicio.precio)
        if self.repo.existe_nombre(servicio.nombre, excluir_id=servicio_id):
            raise ServicioDuplicadoError("Ya existe un servicio con ese nombre.")
        return self.repo.guardar(servicio)

class EliminarServicioUseCase:
    def __init__(self, repo): self.repo = repo
    def ejecutar(self, servicio_id):
        ObtenerServicioUseCase(self.repo).ejecutar(servicio_id)
        if self.repo.esta_en_uso(servicio_id):
            raise ServicioEnUsoError("El servicio aparece en una atención.")
        self.repo.eliminar(servicio_id)
