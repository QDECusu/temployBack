from django.db import models
from django.contrib.auth.models import User
import datetime

# # Create your models here.
# class JobListing(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	company_name = models.CharField(max_length=80)
# 	job_position = models.CharField(max_length=50)
# 	job_phone = models.CharField(max_length=10)
# 	job_email = models.EmailField()
# 	job_description = models.TextField()
# 	job_schedule = models.CharField(max_length=500)
# 	#job_post_date = models.DateField()

# class Profile(models.Model):
# 	user = models.OneToOneField(User, on_delete=models.CASCADE)
# 	zipcode = models.IntegerField(min_value=501, max_length=99950)
# 	rating = models.FloatField(min_value=0.0, max_value=5.0)
# 	skills = models.TextField(null=True)
