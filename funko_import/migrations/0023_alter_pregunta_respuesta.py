# Generated by Django 5.0.3 on 2025-02-23 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funko_import', '0022_alter_pregunta_respuesta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pregunta',
            name='respuesta',
            field=models.TextField(max_length=255, null=True),
        ),
    ]
