from django.db import models
from django.contrib.auth.models import User
from django.core.validators import * 
from .validators import is_json
import datetime
from .modelFunctions import *

# Create your models here.
class JobListing(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	company_name = models.CharField(max_length=80)
	job_position = models.CharField(max_length=50)
	job_phone = models.CharField(max_length=10)
	job_email = models.EmailField(validators=[EmailValidator])
	job_description = models.TextField()
	job_schedule = models.CharField(max_length=500)
	job_post_date = models.DateField(auto_now_add=True)

class AvailabilityListing(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	description = models.TextField(validators=[MinLengthValidator(10)])
	schedule = models.CharField(max_length=500)
	post_date = models.DateField(auto_now_add=True)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	zipcode = models.IntegerField(validators=[MinValueValidator(501), MaxValueValidator(99950)], default=00000)
	rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], default=0)
	skills = models.TextField(blank=True)
	short_description = models.TextField(blank=True)
	image = models.ImageField("Uploaded image", upload_to=scramble_uploaded_filename, blank=True)
	