# Generated by Django 2.0.2 on 2018-03-26 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temploybackend', '0003_joblisting_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='short_description',
            field=models.TextField(null=True),
        ),
    ]
