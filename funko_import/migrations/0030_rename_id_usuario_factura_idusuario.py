# Generated by Django 5.0.3 on 2025-02-26 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('funko_import', '0029_rename_id_producto_resenacomentario_idproducto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='factura',
            old_name='id_Usuario',
            new_name='idUsuario',
        ),
    ]
