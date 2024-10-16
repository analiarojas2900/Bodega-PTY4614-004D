# Generated by Django 5.1 on 2024-10-15 23:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Polls', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='roles',
        ),
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Polls.role'),
        ),
    ]
