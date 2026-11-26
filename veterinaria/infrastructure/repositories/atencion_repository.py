from django.db import transaction

from veterinaria.domain.entities.atencion import Atencion
from veterinaria.domain.entities.detalle_atencion import DetalleAtencion
from veterinaria.domain.repositories.atencion_repository import AtencionRepository
from veterinaria.infrastructure.models.atencion import AtencionModel
from veterinaria.infrastructure.models.detalle_atencion import DetalleAtencionModel

DB = "negocio"


def _detalle(modelo):
    return DetalleAtencion(
        atencion_id=modelo.atencion_id,
        servicio_id=modelo.servicio_id,
        cantidad=modelo.cantidad,
        precio_unitario=modelo.precio_unitario,
    )


def _atencion(modelo):
    detalles = DetalleAtencionModel.objects.using(DB).filter(
        atencion_id=modelo.id
    ).order_by("servicio_id")

    return Atencion(
        id=modelo.id,
        mascota_id=modelo.mascota_id,
        fecha=modelo.fecha,
        motivo=modelo.motivo,
        diagnostico=modelo.diagnostico,
        total=modelo.total,
        estado=modelo.estado,
        detalles=[_detalle(detalle) for detalle in detalles],
    )


class DjangoAtencionRepository(AtencionRepository):
    def listar(self):
        modelos = AtencionModel.objects.using(DB).order_by("-fecha")
        return [_atencion(modelo) for modelo in modelos]

    def obtener_por_id(self, atencion_id):
        modelo = AtencionModel.objects.using(DB).filter(
            id=atencion_id
        ).first()
        return _atencion(modelo) if modelo else None

    def existe_agendada_en_fecha(self, mascota_id, fecha):
        return AtencionModel.objects.using(DB).filter(
            mascota_id=mascota_id,
            estado="AGENDADA",
            fecha__date=fecha,
        ).exists()

    def registrar(self, atencion):
        with transaction.atomic(using=DB):
            valores = {
                "mascota_id": atencion.mascota_id,
                "motivo": atencion.motivo,
                "diagnostico": atencion.diagnostico,
                "total": atencion.total,
                "estado": atencion.estado,
            }
            if atencion.fecha is not None:
                valores["fecha"] = atencion.fecha

            cabecera = AtencionModel.objects.using(DB).create(**valores)

            for detalle in atencion.detalles:
                DetalleAtencionModel.objects.using(DB).create(
                    atencion_id=cabecera.id,
                    servicio_id=detalle.servicio_id,
                    cantidad=detalle.cantidad,
                    precio_unitario=detalle.precio_unitario,
                )

            cabecera.refresh_from_db(using=DB)

        return self.obtener_por_id(cabecera.id)

    def actualizar(self, atencion):
        AtencionModel.objects.using(DB).filter(id=atencion.id).update(
            motivo=atencion.motivo,
            diagnostico=atencion.diagnostico,
        )
        return self.obtener_por_id(atencion.id)

    def cambiar_estado(self, atencion, nuevo_estado):
        AtencionModel.objects.using(DB).filter(id=atencion.id).update(
            estado=nuevo_estado
        )
        return self.obtener_por_id(atencion.id)

    def eliminar(self, atencion_id):
        with transaction.atomic(using=DB):
            DetalleAtencionModel.objects.using(DB).filter(
                atencion_id=atencion_id
            ).delete()
            borrados, _ = AtencionModel.objects.using(DB).filter(
                id=atencion_id
            ).delete()
        return borrados > 0
