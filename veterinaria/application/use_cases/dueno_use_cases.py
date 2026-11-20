from typing import List 
from veterinaria.application.exceptions import ( 
    DuenoConMascotasError, DuenoNoEncontradoError, 
    EmailDuplicadoError, RutDuplicadoError, 
) 
from veterinaria.domain.entities.dueno import Dueno 
from veterinaria.domain.repositories.dueno_repository import DuenoRepository 
 
 
def _validar_unicos(repo, rut, email, excluir_rut=None): 
    if excluir_rut is None and repo.existe_rut(rut): 
        raise RutDuplicadoError(f"Ya existe un dueño con RUT {rut}.") 
    if email and repo.existe_email(email, excluir_rut): 
        raise EmailDuplicadoError(f"Ya existe un dueño con email {email}.") 
 
 
class ListarDuenosUseCase: 
    def __init__(self, repo: DuenoRepository): self.repo = repo 
    def ejecutar(self) -> List[Dueno]: return self.repo.listar() 
 
 
class ObtenerDuenoUseCase: 
    def __init__(self, repo: DuenoRepository): self.repo = repo 
    def ejecutar(self, rut: str) -> Dueno: 
        dueno = self.repo.obtener_por_rut(rut) 
        if dueno is None: 
            raise DuenoNoEncontradoError(f"No existe dueño con RUT {rut}.") 
        return dueno 
 
 
class CrearDuenoUseCase: 
    def __init__(self, repo: DuenoRepository): self.repo = repo 
    def ejecutar(self, datos: dict) -> Dueno: 
        _validar_unicos(self.repo, datos["rut"], datos.get("email")) 
        return self.repo.guardar(Dueno( 
            rut=datos["rut"], nombre=datos["nombre"], 
            telefono=datos.get("telefono"), email=datos.get("email"), 
            direccion=datos.get("direccion"))) 
 
 
class ActualizarDuenoUseCase: 
    def __init__(self, repo: DuenoRepository): self.repo = repo 
    def ejecutar(self, rut: str, datos: dict) -> Dueno: 
        dueno = ObtenerDuenoUseCase(self.repo).ejecutar(rut) 
        dueno.nombre = datos.get("nombre", dueno.nombre) 
        dueno.telefono = datos.get("telefono", dueno.telefono) 
        dueno.email = datos.get("email", dueno.email) 
        dueno.direccion = datos.get("direccion", dueno.direccion) 
        _validar_unicos(self.repo, rut, dueno.email, excluir_rut=rut) 
        return self.repo.guardar(dueno) 
 
 
class EliminarDuenoUseCase: 
    def __init__(self, repo: DuenoRepository): self.repo = repo 
    def ejecutar(self, rut: str) -> None: 
        ObtenerDuenoUseCase(self.repo).ejecutar(rut) 
        if self.repo.tiene_mascotas(rut): 
            raise DuenoConMascotasError( 
                "No se puede eliminar un dueño que tiene mascotas." 
            ) 
        self.repo.eliminar(rut) 