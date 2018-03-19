from django.http import HttpResponse
#For django rest framework (+ serializers)
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins, generics, views
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer, GroupSerializer, JobPostingSerializer, CreateUserSerializer
from .models import JobListing, Profile
import jwt, json
#For Authenticating
from .auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class getUserPostView(views.APIView):
	"""
	API endpoint to get posts assigned to user
	"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		jobList = JobListing.objects.filter(user=request.user.id)
		jData = []
		for job in jobList:
			jData.append({
				'user': job.user.username,
				'company_name': job.company_name,
				'job_position': job.job_position,
				'job_phone': job.job_phone,
				'job_email': job.job_email,
				'job_description': job.job_description,
				'job_schedule': job.job_schedule,
				'job_post_date': str(job.job_post_date)
			})

		return HttpResponse(
			json.dumps(jData),
			status=200,
			content_type="application/json"
		)

class jobPostViewSet(viewsets.ModelViewSet):
	"""
	API endpoint to get posts assigned to user
	"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	serializer_class = JobPostingSerializer
	queryset = JobListing.objects.all()