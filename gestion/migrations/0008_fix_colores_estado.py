from django.db import migrations


def fix_colores(apps, schema_editor):
    EstadoSuministro = apps.get_model('gestion', 'EstadoSuministro')
    EstadoSuministro.objects.filter(estado_suministro__iexact='ASIGNADO').update(color='#007bff')
    EstadoSuministro.objects.filter(estado_suministro__iexact='DEVUELTO').update(color='#ef4444')


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0007_update_color_asignado'),
    ]

    operations = [
        migrations.RunPython(fix_colores, migrations.RunPython.noop),
    ]
