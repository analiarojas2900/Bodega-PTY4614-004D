# Generated by Django 5.1 on 2024-11-11 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Polls', '0015_rename_fecha_ticket_fecha_creacion_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='material',
            old_name='stock_minimo',
            new_name='stock',
        ),
    ]