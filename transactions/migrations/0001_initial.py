# Generated by Django 5.1.3 on 2024-11-12 19:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_emision', models.DateField()),
                ('fecha_vencimiento', models.DateField(blank=True, null=True)),
                ('descuento', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_iva', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estado', models.CharField(default='Activo', max_length=50)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.cliente')),
                ('trabajador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.trabajador')),
            ],
        ),
        migrations.CreateModel(
            name='Detalles_Cotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('subtotal_prodC', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('iva_producto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cotizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.cotizacion')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Proforma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_emision', models.DateField()),
                ('fecha_vencimiento', models.DateField(blank=True, null=True)),
                ('descuento', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_iva', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estado', models.CharField(default='Activo', max_length=50)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.cliente')),
                ('forma_pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.forma_pago')),
                ('medio_pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.medio_pago')),
                ('trabajador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.trabajador')),
            ],
        ),
        migrations.CreateModel(
            name='Detalles_Proforma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('subtotal_prodProf', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('iva_producto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.producto')),
                ('proforma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.proforma')),
            ],
        ),
    ]
