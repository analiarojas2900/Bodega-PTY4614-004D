# Generated by Django 5.1 on 2024-10-29 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Polls', '0005_rename_unidad_medida_material_unidadmedida'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='estado',
            new_name='EstadoTicket',
        ),
    ]