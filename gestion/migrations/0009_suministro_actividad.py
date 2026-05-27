from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0008_fix_colores_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='suministro',
            name='actividad',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='gestion.actividad',
                verbose_name='Actividad',
            ),
        ),
    ]
