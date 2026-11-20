from django.db import models

class ServicioModel(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_servicio")
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = "servicios"
