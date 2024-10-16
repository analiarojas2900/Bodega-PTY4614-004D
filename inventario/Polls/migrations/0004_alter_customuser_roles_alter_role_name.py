# Generated by Django 5.1 on 2024-10-16 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Polls', '0003_remove_customuser_role_customuser_roles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='roles',
            field=models.ManyToManyField(to='Polls.role'),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
