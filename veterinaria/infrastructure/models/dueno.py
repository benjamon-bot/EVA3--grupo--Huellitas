from django.db import models 
from django.db.models.functions import Now 
 
 
class DuenoModel(models.Model): 
    rut = models.CharField(primary_key=True, max_length=12) 
    nombre = models.CharField(max_length=100) 
    telefono = models.CharField(max_length=20, null=True, blank=True) 
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True) 
    direccion = models.CharField(max_length=150, null=True, blank=True) 
    fecha_registro = models.DateTimeField(db_default=Now(), editable=False) 
 
    class Meta: 
        managed = False 
        db_table = "duenos" 
 
    def __str__(self): 
        return f"{self.nombre} ({self.rut})" 