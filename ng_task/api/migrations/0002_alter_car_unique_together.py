# Generated by Django 3.2.5 on 2021-07-16 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='car',
            unique_together={('make', 'model')},
        ),
    ]
