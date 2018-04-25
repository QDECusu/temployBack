from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import JobListing, Profile, AvailabilityListing, Application
from django.contrib.auth.hashers import check_password
from django.conf import settings
import jwt, json
from rest_framework.fields import CurrentUserDefault
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
		profile = Profile.objects.create(user=user)
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

class UserForProfileSerializer(serializers.ModelSerializer):

	is_mod = serializers.SerializerMethodField()
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password', 'first_name', 'last_name', 'is_mod')
		extra_kwargs = {'password': {'write_only': True}}

	def get_is_mod(self, instance):
		return instance.groups.filter(name="Moderators").exists()

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
	user = UserForProfileSerializer()

	class Meta:
		model = Profile
		depth = 1
		fields = ('id', 'user', 'zipcode', 'rating', 'skills', 'short_description', 'image')

	def update(self, instance, validated_data):
		user_data = validated_data.pop('user', {})
		# import ipdb; ipdb.set_trace()
		User.objects.filter(id=instance.user.id).update(**user_data)
		instance = Profile.objects.get(id=instance.id)
		return super(ProfileSerializer, self).update(instance, validated_data)

class ProfilePictureSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ('user', 'image', )

class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')

class JobPostSerializer(serializers.ModelSerializer):
	user = serializers.PrimaryKeyRelatedField(
		default=serializers.CurrentUserDefault(),
		read_only=True
	)

	has_applied = serializers.SerializerMethodField()

	has_accepted = serializers.SerializerMethodField()

	class Meta:
		model = JobListing
		fields = ('id', 'user', 'company_name', 'job_position', 'job_phone', 'job_email', 'job_description', 'job_schedule', 'has_applied', 'has_accepted')

	def create(self, validated_data):
		post = super().create(validated_data)
		post.save()
		return post

	def get_has_applied(self, instance):
		user = self.context['request'].user
		applications = Application.objects.filter(user=user)
		applications = applications.filter(job_listing=instance)
		return applications.exists()

	def get_has_accepted(self, instance):
		user = self.context['request'].user
		applications = Application.objects.filter(user=user)
		application = applications.filter(job_listing=instance).first()

		if application != None:
			return application.accepted
		else:
			return ""

class AvailabilityPostSerializer(serializers.ModelSerializer):
	user = serializers.PrimaryKeyRelatedField(
		default=serializers.CurrentUserDefault(),
		read_only=True
	)

	class Meta:
		model = AvailabilityListing
		fields = ('id', 'user', 'description', 'schedule', 'post_date')

	def create(self, validated_data):
		post = super().create(validated_data)
		post.save()
		return post

class ProfileField(serializers.RelatedField):
	def to_representation(self, value):
		user = value
		profile = Profile.objects.filter(user=user.id).first()
		jData = {
			'id': int(profile.id),
			'username': str(user.username),
			'first_name': str(user.first_name),
			'last_name': str(user.last_name),
			'email': str(user.email),
			'Group': str(user.groups),
			'zipcode': profile.zipcode,
			'rating':profile.rating,
			'skills': profile.skills,
			'short_description': profile.short_description
		}
		return json.dumps(jData)

class ApplicationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Application
		fields = ('user', 'job_listing', 'accepted')

	def create(self, validated_data):
		user = self.request.user
		User.objects.filter(id=instance.user.id).update(**user_data)
		instance = Profile.objects.get(id=instance.id)
		return super(ProfileSerializer, self).update(instance, validated_data)