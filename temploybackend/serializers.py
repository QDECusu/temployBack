from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import JobListing, Profile

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'username', 'email', 'password', 'first_name', 'last_name')
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		user = super().create(validated_data)
		user.set_password(user.password)
		user.save()
		return user

class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')

class JobPostingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = JobListing
		fields = ('user', 'company_name', 'job_position', 'job_phone', 'job_email', 'job_description', 'job_schedule', 'job_post_date')

	# def create(self, validated_data):
	# 	user = super().create(validated_data)
	# 	user.set_password(user.password)
	# 	user.save()
	# 	return user