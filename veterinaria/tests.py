from datetime import datetime

from veterinaria.application.exceptions import (
    AtencionDuplicadaError,
    CambioEstadoInvalidoError,
)
from veterinaria.application.use_cases.atencion_use_cases import (
    CambiarEstadoAtencionUseCase,
    CrearAtencionUseCase,
    ObtenerAtencionUseCase,
)
from veterinaria.infrastructure.di import (
    get_atencion_repository,
    get_mascota_repository,
    get_servicio_repository,
)


def ejecutar_pruebas_semana3(mascota_id, servicio_id):
    atenciones = get_atencion_repository()
    mascotas = get_mascota_repository()
    servicios = get_servicio_repository()

    crear = CrearAtencionUseCase(atenciones, mascotas, servicios)
    datos = {
        "mascota_id": mascota_id,
        "fecha": datetime.now(),
        "motivo": "Control general",
        "detalles": [{"servicio_id": servicio_id, "cantidad": 1}],
    }

    creada = crear.ejecutar(datos)
    print("CREADA:", creada)
    print("TOTAL:", creada.total)

    consultada = ObtenerAtencionUseCase(atenciones).ejecutar(creada.id)
    print("DETALLES:", consultada.detalles)

    try:
        crear.ejecutar(datos)
    except AtencionDuplicadaError as error:
        print("R1 CORRECTA:", error)

    cambiar = CambiarEstadoAtencionUseCase(atenciones)
    print("REALIZADA:", cambiar.ejecutar(creada.id, "REALIZADA").estado)
    print("PAGADA:", cambiar.ejecutar(creada.id, "PAGADA").estado)

    try:
        cambiar.ejecutar(creada.id, "AGENDADA")
    except CambioEstadoInvalidoError as error:
        print("TRANSICIÓN BLOQUEADA:", error)

