from django.contrib import admin

from veterinaria.infrastructure.models import (
    AtencionModel,
    DuenoModel,
    MascotaModel,
    ServicioModel,
)


@admin.register(DuenoModel)
class DuenoAdmin(admin.ModelAdmin):
    list_display = (
        "rut", "nombre", "telefono", "email",
        "direccion", "fecha_registro",
    )
    list_display_links = ("rut", "nombre")
    search_fields = ("rut", "nombre", "email")
    ordering = ("nombre",)


@admin.register(MascotaModel)
class MascotaAdmin(admin.ModelAdmin):
    list_display = (
        "id", "nombre", "especie", "raza",
        "dueno", "sexo", "activo",
    )
    list_filter = ("especie", "sexo", "activo")
    search_fields = (
        "nombre", "dueno__rut", "dueno__nombre",
    )
    ordering = ("nombre",)


@admin.register(ServicioModel)
class ServicioAdmin(admin.ModelAdmin):
    list_display = (
        "id", "nombre", "descripcion", "precio", "activo",
    )
    list_filter = ("activo",)
    search_fields = ("nombre",)
    ordering = ("nombre",)


@admin.register(AtencionModel)
class AtencionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "mascota", "fecha", "motivo",
        "total", "estado", "lineas",
    )
    list_filter = ("estado", "fecha")
    search_fields = (
        "mascota__nombre", "motivo", "diagnostico",
    )
    readonly_fields = (
        "mascota", "fecha", "motivo", "diagnostico",
        "total", "estado", "lineas",
    )
    ordering = ("-id",)

    @admin.display(description="Servicios realizados")
    def lineas(self, obj):
        return ", ".join(
            f"{detalle.servicio.nombre} x {detalle.cantidad} "
            f"= ${detalle.subtotal}"
            for detalle in obj.detalles.select_related("servicio")
        )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
