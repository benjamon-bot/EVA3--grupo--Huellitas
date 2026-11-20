from django.db import models
from .dueno import DuenoModel

class MascotaModel(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_mascota")
    dueno = models.ForeignKey(
        DuenoModel, on_delete=models.PROTECT,
        db_column="rut_dueno", related_name="mascotas")
    nombre = models.CharField(max_length=80)
    especie = models.CharField(max_length=30)
    raza = models.CharField(max_length=60, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=10, null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = "mascotas"
