# Generated by Django 4.0.2 on 2022-02-15 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Registeration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile', models.PositiveIntegerField(blank=True, null=True)),
                ('password', models.CharField(blank=True, max_length=8, null=True)),
            ],
        ),
    ]
