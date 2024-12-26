# Generated by Django 5.0.3 on 2024-12-26 18:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funko_import', '0002_rename_id_usuario_factura_id_usuario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='descuento',
            name='porcentaje',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='promocion',
            name='porcentaje',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
        ),
    ]
