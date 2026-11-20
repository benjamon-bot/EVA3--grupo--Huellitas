from veterinaria.infrastructure.repositories import (
    DjangoDuenoRepository, DjangoMascotaRepository, DjangoServicioRepository,
)

def get_dueno_repository(): return DjangoDuenoRepository()
def get_mascota_repository(): return DjangoMascotaRepository()
def get_servicio_repository(): return DjangoServicioRepository()






