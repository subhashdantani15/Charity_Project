# Generated by Django 4.0.2 on 2022-02-16 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_categorytype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorytype',
            name='image',
            field=models.ImageField(upload_to='donation/'),
        ),
    ]
