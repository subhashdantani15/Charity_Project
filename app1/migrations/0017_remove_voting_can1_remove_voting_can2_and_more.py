# Generated by Django 4.1.2 on 2023-06-20 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0016_voting_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voting',
            name='can1',
        ),
        migrations.RemoveField(
            model_name='voting',
            name='can2',
        ),
        migrations.DeleteModel(
            name='UserVote',
        ),
        migrations.DeleteModel(
            name='Voting',
        ),
    ]
