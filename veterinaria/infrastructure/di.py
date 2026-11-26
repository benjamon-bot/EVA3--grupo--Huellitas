from veterinaria.infrastructure.repositories import (
    DjangoAtencionRepository,
    DjangoDetalleAtencionRepository,
    DjangoDuenoRepository,
    DjangoMascotaRepository,
    DjangoServicioRepository,
)


def get_dueno_repository():
    return DjangoDuenoRepository()


def get_mascota_repository():
    return DjangoMascotaRepository()


def get_servicio_repository():
    return DjangoServicioRepository()


def get_atencion_repository():
    return DjangoAtencionRepository()


def get_detalle_atencion_repository():
    return DjangoDetalleAtencionRepository()