from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import JobListing, Profile
from django.contrib.auth.hashers import check_password
from django.conf import settings
import jwt, json
from .toDict import *

class CreateUserSerializer(serializers.HyperlinkedModelSerializer):
	token = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = ('url', 'username', 'email', 'password', 'first_name', 'last_name', 'token')
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		user = super().create(validated_data)
		user.set_password(user.password)
		user.save()
		return user

	def get_token(self, instance):	
		user = User.objects.get(username=instance.username)	
		payload = {
			'id': user.id,
			'email': user.email,
		}
		jwt_token = jwt.encode(payload, settings.SECRET_KEY).decode("utf-8")

		return str(jwt_token)

class UserSerializer(serializers.HyperlinkedModelSerializer):
	
	class Meta:
		model = User
		fields = ('url', 'username', 'email', 'password', 'first_name', 'last_name')
		extra_kwargs = {'password': {'write_only': True}}

class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')

class JobPostingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = JobListing
		fields = ('user', 'company_name', 'job_position', 'job_phone', 'job_email', 'job_description', 'job_schedule', 'job_post_date')