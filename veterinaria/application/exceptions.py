class NoEncontradoError(Exception): pass
class DuplicadoError(Exception): pass
class ReglaNegocioError(Exception): pass

class DuenoNoEncontradoError(NoEncontradoError): pass
class RutDuplicadoError(DuplicadoError): pass
class EmailDuplicadoError(DuplicadoError): pass
class DuenoConMascotasError(ReglaNegocioError): pass

class MascotaNoEncontradaError(NoEncontradoError): pass
class DuenoRelacionadoNoEncontradoError(NoEncontradoError): pass
class MascotaConAtencionesError(ReglaNegocioError): pass
class EspecieInvalidaError(ReglaNegocioError): pass
class SexoInvalidoError(ReglaNegocioError): pass

class ServicioNoEncontradoError(NoEncontradoError): pass
class ServicioDuplicadoError(DuplicadoError): pass
class PrecioServicioInvalidoError(ReglaNegocioError): pass
class ServicioEnUsoError(ReglaNegocioError): pass
class ServicioInactivoError(ReglaNegocioError): pass

class AtencionNoEncontradaError(NoEncontradoError): pass
class AtencionDuplicadaError(ReglaNegocioError): pass
class AtencionInvalidaError(ReglaNegocioError): pass
class CambioEstadoInvalidoError(ReglaNegocioError): pass
class CantidadDetalleInvalidaError(AtencionInvalidaError): pass
class PrecioDetalleInvalidoError(AtencionInvalidaError): pass
class AtencionSinDetallesError(AtencionInvalidaError): pass
