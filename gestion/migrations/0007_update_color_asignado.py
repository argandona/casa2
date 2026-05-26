from django.db import migrations


def set_color_asignado(apps, schema_editor):
    EstadoSuministro = apps.get_model('gestion', 'EstadoSuministro')
    EstadoSuministro.objects.filter(estado_suministro__iexact='ASIGNADO').update(color='#ef4444')


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0006_estadoliquidacion_sst_estado_liquidacion'),
    ]

    operations = [
        migrations.RunPython(set_color_asignado, migrations.RunPython.noop),
    ]
