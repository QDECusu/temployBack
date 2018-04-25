from django.http import HttpResponse
import json
#For django rest framework (+ serializers)
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, views
from rest_framework import permissions
from .serializers import UserSerializer, AvailabilityPostSerializer
from .models import AvailabilityListing
#For Authenticating
from .auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin, IsOwnerOrAdminOrMod, IsAdminOrMod

class getUserPostView(views.APIView):
	"""
	API endpoint to get posts assigned to user
	"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		availList = AvailabilityListing.objects.filter(user=request.user)
		jData = []
		for post in availList:
			jData.append({
				'id' : post.id,
				'user_id' : post.user.id,
				'user': post.user.username,
				'description' : post.description,
				'schedule' : post.schedule,
				'post_date' : str(post.post_date)
			})

		return HttpResponse(
			json.dumps(jData),
			status=200,
			content_type="application/json"
		)

class availabilityPostViewSet(viewsets.ModelViewSet):
	"""
	API endpoint to get posts assigned to user
	"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	serializer_class = AvailabilityPostSerializer

	def get_queryset(self):
		if self.request.method in permissions.SAFE_METHODS:
			return AvailabilityListing.objects.exclude(user=self.request.user)
		elif IsAdminOrMod(self.request) and self.request.method not in permissions.SAFE_METHODS:
			return AvailabilityListing.objects.all()
		else:
			return AvailabilityListing.objects.filter(user=self.request.user)