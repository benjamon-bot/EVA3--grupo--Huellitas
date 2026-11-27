from django.urls import path

from veterinaria.adaptadores.views import (
    AtencionDetailView,
    AtencionListCreateView,
    DuenoDetailView,
    DuenoListCreateView,
    MascotaDetailView,
    MascotaListCreateView,
    ServicioDetailView,
    ServicioListCreateView,
)


urlpatterns = [
    path(
        "duenos/",
        DuenoListCreateView.as_view(),
        name="dueno-list-create",
    ),
    path(
        "duenos/<str:rut>/",
        DuenoDetailView.as_view(),
        name="dueno-detail",
    ),
    path(
        "mascotas/",
        MascotaListCreateView.as_view(),
        name="mascota-list-create",
    ),
    path(
        "mascotas/<int:mascota_id>/",
        MascotaDetailView.as_view(),
        name="mascota-detail",
    ),
    path(
        "servicios/",
        ServicioListCreateView.as_view(),
        name="servicio-list-create",
    ),
    path(
        "servicios/<int:servicio_id>/",
        ServicioDetailView.as_view(),
        name="servicio-detail",
    ),
    path(
        "atenciones/",
        AtencionListCreateView.as_view(),
        name="atencion-list-create",
    ),
    path(
        "atenciones/<int:atencion_id>/",
        AtencionDetailView.as_view(),
        name="atencion-detail",
    ),
]
