# Generated by Django 5.1 on 2024-11-10 23:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Polls', '0012_alter_customuser_roles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='unidad_medida',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Polls.unidadmedida'),
        ),
    ]
