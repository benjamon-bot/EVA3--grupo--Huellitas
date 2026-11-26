from datetime import date
from decimal import Decimal

from veterinaria.application.exceptions import (
    AtencionDuplicadaError,
    AtencionNoEncontradaError,
    AtencionSinDetallesError,
    CambioEstadoInvalidoError,
    CantidadDetalleInvalidaError,
    MascotaNoEncontradaError,
    PrecioDetalleInvalidoError,
    ServicioInactivoError,
    ServicioNoEncontradoError,
)
from veterinaria.domain.entities.atencion import ESTADOS_ATENCION, Atencion
from veterinaria.domain.entities.detalle_atencion import DetalleAtencion


def _fecha_regla(fecha):
    return fecha.date() if fecha is not None else date.today()


def _crear_detalle(datos, servicios):
    cantidad = int(datos["cantidad"])

    if cantidad <= 0:
        raise CantidadDetalleInvalidaError(
            "La cantidad debe ser mayor que cero."
        )

    servicio = servicios.obtener_por_id(
        int(datos["servicio_id"])
    )

    if servicio is None:
        raise ServicioNoEncontradoError(
            "El servicio indicado no existe."
        )

    if not servicio.activo:
        raise ServicioInactivoError(
            f"El servicio {servicio.nombre} está inactivo."
        )

    precio = Decimal(str(servicio.precio))

    if precio < Decimal("0"):
        raise PrecioDetalleInvalidoError(
            "El precio unitario no puede ser negativo."
        )

    return DetalleAtencion(
        servicio_id=servicio.id,
        cantidad=cantidad,
        precio_unitario=precio,
    )


class ListarAtencionesUseCase:
    def __init__(self, repo):
        self.repo = repo

    def ejecutar(self):
        return self.repo.listar()


class ObtenerAtencionUseCase:
    def __init__(self, repo):
        self.repo = repo

    def ejecutar(self, atencion_id):
        atencion = self.repo.obtener_por_id(atencion_id)

        if atencion is None:
            raise AtencionNoEncontradaError(
                f"No existe una atención con id {atencion_id}."
            )

        return atencion


class CrearAtencionUseCase:
    def __init__(self, repo, mascotas, servicios):
        self.repo = repo
        self.mascotas = mascotas
        self.servicios = servicios

    def ejecutar(self, datos):
        mascota_id = int(datos["mascota_id"])
        fecha = datos.get("fecha")

        if self.mascotas.obtener_por_id(mascota_id) is None:
            raise MascotaNoEncontradaError(
                "La mascota indicada no existe."
            )

        if self.repo.existe_agendada_en_fecha(
            mascota_id,
            _fecha_regla(fecha),
        ):
            raise AtencionDuplicadaError(
                "La mascota ya tiene una atención AGENDADA ese día."
            )

        detalles_datos = datos.get("detalles", [])

        if not detalles_datos:
            raise AtencionSinDetallesError(
                "Debe incluir al menos un servicio."
            )

        detalles = [
            _crear_detalle(detalle, self.servicios)
            for detalle in detalles_datos
        ]

        atencion = Atencion(
            mascota_id=mascota_id,
            motivo=datos["motivo"],
            diagnostico=datos.get("diagnostico"),
            fecha=fecha,
            estado="AGENDADA",
            detalles=detalles,
        )
        atencion.recalcular_total()

        return self.repo.registrar(atencion)


class ActualizarAtencionUseCase:
    def __init__(self, repo):
        self.repo = repo

    def ejecutar(self, atencion_id, datos):
        atencion = ObtenerAtencionUseCase(
            self.repo
        ).ejecutar(atencion_id)

        atencion.motivo = datos.get(
            "motivo",
            atencion.motivo,
        )
        atencion.diagnostico = datos.get(
            "diagnostico",
            atencion.diagnostico,
        )

        return self.repo.actualizar(atencion)


class CambiarEstadoAtencionUseCase:
    def __init__(self, repo):
        self.repo = repo

    def ejecutar(self, atencion_id, nuevo_estado):
        atencion = ObtenerAtencionUseCase(
            self.repo
        ).ejecutar(atencion_id)

        nuevo_estado = nuevo_estado.upper()

        if nuevo_estado not in ESTADOS_ATENCION:
            raise CambioEstadoInvalidoError(
                "El estado solicitado no existe."
            )

        if not atencion.puede_pasar_a(nuevo_estado):
            raise CambioEstadoInvalidoError(
                f"No se puede pasar de {atencion.estado} "
                f"a {nuevo_estado}."
            )

        return self.repo.cambiar_estado(
            atencion,
            nuevo_estado,
        )


class EliminarAtencionUseCase:
    def __init__(self, repo):
        self.repo = repo

    def ejecutar(self, atencion_id):
        atencion = ObtenerAtencionUseCase(
            self.repo
        ).ejecutar(atencion_id)

        if atencion.estado != "AGENDADA":
            raise CambioEstadoInvalidoError(
                "Solo se puede eliminar una atención AGENDADA."
            )

        self.repo.eliminar(atencion_id)
