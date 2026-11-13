-- ============================================================
-- G02 - CLINICA VETERINARIA HUELLITAS
-- Script 02: datos de ejemplo
-- ============================================================


-- ============================================================
-- DUENOS
-- ============================================================

INSERT INTO duenos (
    rut,
    nombre,
    telefono,
    email,
    direccion
)
VALUES (
    '11111111-1',
    'Ana Rojas Soto',
    '+56911111111',
    'ana.rojas@correo.cl',
    'Av. Brasil 123, Santiago'
);


INSERT INTO duenos (
    rut,
    nombre,
    telefono,
    email,
    direccion
)
VALUES (
    '22222222-2',
    'Benjamin Munoz Diaz',
    '+56922222222',
    'benjamin.munoz@correo.cl',
    'Los Carrera 456, Concepcion'
);


INSERT INTO duenos (
    rut,
    nombre,
    telefono,
    email,
    direccion
)
VALUES (
    '33333333-3',
    'Camila Perez Lagos',
    '+56933333333',
    'camila.perez@correo.cl',
    'Av. Central 789, Santiago'
);


-- ============================================================
-- MASCOTAS
-- ============================================================

INSERT INTO mascotas (
    rut_dueno,
    nombre,
    especie,
    raza,
    fecha_nacimiento,
    sexo,
    activo
)
VALUES (
    '11111111-1',
    'Luna',
    'PERRO',
    'Labrador',
    DATE '2021-04-15',
    'HEMBRA',
    1
);


INSERT INTO mascotas (
    rut_dueno,
    nombre,
    especie,
    raza,
    fecha_nacimiento,
    sexo,
    activo
)
VALUES (
    '22222222-2',
    'Milo',
    'GATO',
    'Siames',
    DATE '2022-08-10',
    'MACHO',
    1
);


INSERT INTO mascotas (
    rut_dueno,
    nombre,
    especie,
    raza,
    fecha_nacimiento,
    sexo,
    activo
)
VALUES (
    '33333333-3',
    'Copito',
    'CONEJO',
    NULL,
    DATE '2023-01-20',
    'MACHO',
    1
);


-- ============================================================
-- SERVICIOS
-- ============================================================

INSERT INTO servicios (
    nombre,
    descripcion,
    precio,
    activo
)
VALUES (
    'Consulta general',
    'Evaluacion general realizada por la clinica veterinaria',
    20000,
    1
);


INSERT INTO servicios (
    nombre,
    descripcion,
    precio,
    activo
)
VALUES (
    'Vacunacion',
    'Aplicacion de vacuna indicada para la mascota',
    15000,
    1
);


INSERT INTO servicios (
    nombre,
    descripcion,
    precio,
    activo
)
VALUES (
    'Desparasitacion',
    'Tratamiento de desparasitacion interna o externa',
    12000,
    1
);


INSERT INTO servicios (
    nombre,
    descripcion,
    precio,
    activo
)
VALUES (
    'Corte de unas',
    'Corte y revision de las unas de la mascota',
    8000,
    1
);


-- ============================================================
-- ATENCION DE EJEMPLO PARA LUNA
-- Se registra una atencion realizada por un total de 35000.
-- ============================================================

INSERT INTO atenciones (
    id_mascota,
    motivo,
    diagnostico,
    total,
    estado
)
SELECT
    id_mascota,
    'Control general y vacunacion',
    'Mascota en buenas condiciones generales',
    35000,
    'REALIZADA'
FROM mascotas
WHERE nombre = 'Luna'
AND rut_dueno = '11111111-1';


-- ============================================================
-- DETALLE 1: CONSULTA GENERAL
-- ============================================================

INSERT INTO detalle_atencion (
    id_atencion,
    id_servicio,
    cantidad,
    precio_unitario
)
SELECT
    a.id_atencion,
    s.id_servicio,
    1,
    s.precio
FROM atenciones a
INNER JOIN mascotas m
    ON m.id_mascota = a.id_mascota
CROSS JOIN servicios s
WHERE m.nombre = 'Luna'
AND m.rut_dueno = '11111111-1'
AND s.nombre = 'Consulta general';


-- ============================================================
-- DETALLE 2: VACUNACION
-- ============================================================

INSERT INTO detalle_atencion (
    id_atencion,
    id_servicio,
    cantidad,
    precio_unitario
)
SELECT
    a.id_atencion,
    s.id_servicio,
    1,
    s.precio
FROM atenciones a
INNER JOIN mascotas m
    ON m.id_mascota = a.id_mascota
CROSS JOIN servicios s
WHERE m.nombre = 'Luna'
AND m.rut_dueno = '11111111-1'
AND s.nombre = 'Vacunacion';


-- Confirma todos los cambios.

COMMIT;