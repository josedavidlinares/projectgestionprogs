# Generated by Django 5.1.3 on 2024-11-12 19:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Forma_Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Medio_Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_producto', models.CharField(max_length=50, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('marca', models.CharField(blank=True, max_length=100, null=True)),
                ('stock', models.IntegerField(default=0)),
                ('stock_min', models.IntegerField(default=0)),
                ('stock_max', models.IntegerField(default=0)),
                ('precio_venta', models.DecimalField(decimal_places=2, max_digits=10)),
                ('mercancia_muerta', models.BooleanField(default=False)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('cantidad', models.IntegerField()),
                ('n_lote', models.CharField(blank=True, max_length=50, null=True)),
                ('precio_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.proveedor')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Historico_Precios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_cambio', models.DateField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Ajuste_Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('motivo', models.CharField(max_length=255)),
                ('fecha', models.DateField()),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.producto')),
            ],
        ),
    ]