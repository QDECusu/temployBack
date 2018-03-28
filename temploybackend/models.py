from django.db import models
from django.contrib.auth.models import User
from django.core.validators import * 
import datetime

# Create your models here.
class JobListing(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	company_name = models.CharField(max_length=80, default ='company name')
	job_position = models.CharField(max_length=50, default ='job position')
	job_phone = models.CharField(max_length=10, default ='0000000000')
	job_email = models.EmailField(default ='123@abc.com')
	job_description = models.TextField(default ='job description')
	job_schedule = models.CharField(max_length=500, default = 'schedule')
	job_post_date = models.DateField(auto_now_add=True)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	zipcode = models.IntegerField(validators=[MinValueValidator(501), MaxValueValidator(99950)], default=00000)
	rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], default=0)
	skills = models.TextField(blank=True, default = 'skills')
	short_description = models.TextField(blank=True, default = 'short description')
	