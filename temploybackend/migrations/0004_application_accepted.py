# Generated by Django 2.0.4 on 2018-04-24 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temploybackend', '0003_auto_20180423_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]