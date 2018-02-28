from django.contrib.auth.models import User, Group
from rest_framework import serializers

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