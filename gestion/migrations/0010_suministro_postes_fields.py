from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0009_suministro_actividad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suministro',
            name='no_ot',
            field=models.CharField(blank=True, max_length=20, verbose_name='N° OT'),
        ),
        migrations.AlterField(
            model_name='suministro',
            name='direccion',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='suministro',
            name='placa_camion',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='suministros',
                to='gestion.unidadtransporte',
                verbose_name='Placa del Camión',
            ),
        ),
    ]
