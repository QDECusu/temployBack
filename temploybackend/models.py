from django.db import models

# Create your models here.
class JobListing(models.Model):
    company_name = models.CharField(max_length=500)
    job_position = models.CharField(max_length=250)
    job_phone = models.CharField(max_length=10)
    job_email = models.EmailField()
    job_description = models.TextField()
    job_schedule = models.CharField(max_length=500)
    job_post_date = models.DateField()

