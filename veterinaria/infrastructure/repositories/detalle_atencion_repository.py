from veterinaria.domain.entities.detalle_atencion import DetalleAtencion
from veterinaria.domain.repositories.detalle_atencion_repository import (
    DetalleAtencionRepository,
)
from veterinaria.infrastructure.models.detalle_atencion import (
    DetalleAtencionModel,
)

DB = "negocio"


def _to_entity(modelo):
    return DetalleAtencion(
        atencion_id=modelo.atencion_id,
        servicio_id=modelo.servicio_id,
        cantidad=modelo.cantidad,
        precio_unitario=modelo.precio_unitario,
    )


class DjangoDetalleAtencionRepository(DetalleAtencionRepository):
    def listar_por_atencion(self, atencion_id):
        modelos = DetalleAtencionModel.objects.using(DB).filter(
            atencion_id=atencion_id
        ).order_by("servicio_id")
        return [_to_entity(modelo) for modelo in modelos]

    def guardar(self, detalle):
        modelo = DetalleAtencionModel.objects.using(DB).create(
            atencion_id=detalle.atencion_id,
            servicio_id=detalle.servicio_id,
            cantidad=detalle.cantidad,
            precio_unitario=detalle.precio_unitario,
        )
        return _to_entity(modelo)

    def eliminar_por_atencion(self, atencion_id):
        borrados, _ = DetalleAtencionModel.objects.using(DB).filter(
            atencion_id=atencion_id
        ).delete()
        return borrados

    def servicio_esta_en_uso(self, servicio_id):
        return DetalleAtencionModel.objects.using(DB).filter(
            servicio_id=servicio_id
        ).exists()
