from django.db import models
from django.db.models.functions import Now
from .mascota import MascotaModel

class AtencionModel(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_atencion")
    mascota = models.ForeignKey(
        MascotaModel, on_delete=models.PROTECT,
        db_column="id_mascota", related_name="atenciones")
    fecha = models.DateTimeField(db_default=Now(), editable=False)
    motivo = models.CharField(max_length=200)
    diagnostico = models.CharField(max_length=500, null=True, blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, default="AGENDADA")

    class Meta:
        managed = False
        db_table = "atenciones"
