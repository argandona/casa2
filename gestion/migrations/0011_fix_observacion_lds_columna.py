from django.db import migrations


TABLA = 'gestion_suministro'
ACENTUADA = 'Observación_LDS'
OBJETIVO = 'Observacion_LDS'


def _columnas(schema_editor):
    conn = schema_editor.connection
    with conn.cursor() as cursor:
        return [c.name for c in conn.introspection.get_table_description(cursor, TABLA)]


def renombrar_a_sin_tilde(apps, schema_editor):
    """Renombra la columna con tilde a la versión sin tilde, SOLO si hace falta.

    - Entornos nuevos (BD construida desde migraciones): la columna quedó como
      'Observación_LDS' y se renombra a 'Observacion_LDS'.
    - Producción: la columna ya existe sin tilde, así que esto no hace nada.
    """
    cols = _columnas(schema_editor)
    if ACENTUADA in cols and OBJETIVO not in cols:
        schema_editor.execute(
            f'ALTER TABLE {TABLA} RENAME COLUMN "{ACENTUADA}" TO "{OBJETIVO}"'
        )


def revertir_a_con_tilde(apps, schema_editor):
    cols = _columnas(schema_editor)
    if OBJETIVO in cols and ACENTUADA not in cols:
        schema_editor.execute(
            f'ALTER TABLE {TABLA} RENAME COLUMN "{OBJETIVO}" TO "{ACENTUADA}"'
        )


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0010_suministro_postes_fields'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RenameField(
                    model_name='suministro',
                    old_name='Observación_LDS',
                    new_name='Observacion_LDS',
                ),
            ],
            database_operations=[
                migrations.RunPython(renombrar_a_sin_tilde, revertir_a_con_tilde),
            ],
        ),
    ]
