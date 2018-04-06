# Generated by Django 2.0.4 on 2018-04-06 04:52

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailabilityListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(validators=[django.core.validators.MinLengthValidator(10)])),
                ('schedule', models.CharField(max_length=500)),
                ('post_date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JobListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=80)),
                ('job_position', models.CharField(max_length=50)),
                ('job_phone', models.CharField(max_length=10)),
                ('job_email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator])),
                ('job_description', models.TextField()),
                ('job_schedule', models.CharField(max_length=500)),
                ('job_post_date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zipcode', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(501), django.core.validators.MaxValueValidator(99950)])),
                ('rating', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('skills', models.TextField(blank=True)),
                ('short_description', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
