# Generated by Django 4.0.2 on 2022-03-08 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_registeration_is_voted_uservote'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('password', models.CharField(blank=True, max_length=8, null=True)),
            ],
        ),
    ]