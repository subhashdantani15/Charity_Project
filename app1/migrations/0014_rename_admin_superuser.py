# Generated by Django 4.0.2 on 2022-03-08 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_admin'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Admin',
            new_name='Superuser',
        ),
    ]
