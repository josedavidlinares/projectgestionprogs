# Generated by Django 5.1.3 on 2024-11-13 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_cliente_id_alter_estado_region_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trabajador',
            name='documento_trabajador',
            field=models.CharField(max_length=20),
        ),
    ]