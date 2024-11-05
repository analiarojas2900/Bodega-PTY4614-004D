# Generated by Django 5.1 on 2024-11-05 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Polls', '0010_alter_customuser_roles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='roles',
            field=models.ManyToManyField(blank=True, to='Polls.role'),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
