BEGIN;

ALTER TABLE estudiantes
    ADD COLUMN IF NOT EXISTS observaciones text;

ALTER TABLE profesores
    ADD COLUMN IF NOT EXISTS programa text,
    ADD COLUMN IF NOT EXISTS asignaturas text,
    ADD COLUMN IF NOT EXISTS horas_dedicacion integer,
    ADD COLUMN IF NOT EXISTS observaciones text;

COMMIT;
