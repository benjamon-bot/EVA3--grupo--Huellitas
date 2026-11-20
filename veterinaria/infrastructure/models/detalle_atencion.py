from django.db import models
from .atencion import AtencionModel
from .servicio import ServicioModel

class DetalleAtencionModel(models.Model):
    pk = models.CompositePrimaryKey("atencion", "servicio")
    atencion = models.ForeignKey(
        AtencionModel, on_delete=models.CASCADE,
        db_column="id_atencion", related_name="detalles")
    servicio = models.ForeignKey(
        ServicioModel, on_delete=models.PROTECT,
        db_column="id_servicio", related_name="detalles_atencion")
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.GeneratedField(
        expression=models.F("cantidad") * models.F("precio_unitario"),
        output_field=models.DecimalField(max_digits=12, decimal_places=2),
        db_persist=False)

    class Meta:
        managed = False
        db_table = "detalle_atencion"
