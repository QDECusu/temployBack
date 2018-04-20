from django.http import HttpResponse
from django.http import HttpRequest
#For login portion
import jwt, json
from rest_framework import views
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.conf import settings
from .toDict import to_dict

#For Authenticating
from .auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#For django rest framework (+ serializers)
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins, generics
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer, GroupSerializer, JobPostSerializer, CreateUserSerializer, ProfileSerializer, AvailabilityPostSerializer, ProfilePictureSerializer, ApplicationSerializer
from .models import JobListing, Profile, AvailabilityListing, Application
from drf_multiple_model.views import ObjectMultipleModelAPIView

class Home(views.APIView):

	def get(self, request):
		return HttpResponse("The home route works")

class TestUserViewNoAuth(viewsets.ModelViewSet):
	"""
	API endpoint that allows a user to be viewed without authentication
	1. Create a Superuser using the manage.py
	2. Create a User from the admin panel
	"""
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer

class TestAuth(viewsets.ModelViewSet):
	"""
	API endpoint that allows a user to be viewed with authentication
	1. Create a Superuser using the manage.py
	2. Create a User from the admin panel (If desired, not nessesarily required)
	3. Make a Post request to hostname/getUserJsonAuth/ with the following in the headers
	key = Authorization
	data = Token with your JWT from the login
	"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer

class TestSimpleUserJson(views.APIView):
	"""
	API endpoint that allows a user to be viewed without authentication, and outputs the first user
	1. Create a Superuser using the manage.py
	2. Create a User from the admin panel
	"""

	def get(self, request, *args, **kwargs):
		user = User.objects.filter(id=1).first()
		jData = {
			'id': int(user.id),
			'username': str(user.username),
			'email': str(user.email),
			'Group': str(user.groups)
		}

		return HttpResponse(
			json.dumps(jData),
			status=200,
			content_type="application/json"
		)

class TestSimpleUserJsonAuth(views.APIView):
	"""
	API endpoint that allows a user to be viewed with authentication, and outputs the authed user
	1. Create a Superuser using the manage.py
	2. Create a User from the admin panel (If desired, not nessesarily required)
	3. Make a Post request to hostname/getUserJsonAuth/ with the following in the headers
	key = Authorization
	data = Token with your JWT from the login
	"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def post(self, request, *args, **kwargs):
		user = request.user
		jData = {
			'id': int(user.id),
			'username': str(user.username),
			'first_name': str(user.first_name),
			'last_name': str(user.last_name),
			'email': str(user.email),
			'Group': str(user.groups)
		}

		return HttpResponse(
			json.dumps(jData),
			status=200,
			content_type="application/json"
		)

class Login(views.APIView):

	def post(self, request, *args, **kwargs):
		if not request.data:
			return Response({'Error': "Please provide username/password"}, status="400")
		
		username = request.data['username']
		password = request.data['password']
		
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			return Response({'Error': "Invalid username/password"}, status="400")
		passCheck = check_password(password, user.password)
		if not passCheck:
			return Response({'Error': "Invalid username/password"}, status="400")
		if passCheck:		
			payload = {
				'id': user.id,
				'email': user.email,
			}
			jwt_token = {'token': jwt.encode(payload, settings.SECRET_KEY).decode("utf-8") }

			return HttpResponse(json.dumps(jwt_token))

			return HttpResponse(
			  json.dumps(jwt_token),
			  status=200,
			  content_type="application/json"
			)
		else:
			return Response(
			  json.dumps({'Error': "Invalid credentials"}),
			  status=400,
			  content_type="application/json"
			)

class CreateUserView(generics.CreateAPIView):
	"""
	API endpoint that allows a user to be created
	"""
	#queryset = ''
	serializer_class = CreateUserSerializer

class ProfileView(viewsets.ModelViewSet):
	"""
	API endpoint that allows a user to be viewed with authentication
	1. Create a Superuser using the manage.py
	2. Create a User from the admin panel (If desired, not nessesarily required)
	3. Make a Post request to hostname/getUserJsonAuth/ with the following in the headers
	key = Authorization
	data = Token with your JWT from the login
	"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	serializer_class = ProfileSerializer

	def get_queryset(self):
		if self.request.method in permissions.SAFE_METHODS:
			return Profile.objects.all()
		return Profile.objects.filter(user=self.request.user)

class UserProfileView(views.APIView):
	"""
	API Endpoint that allows a user to view their own profile information
	"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request, *args, **kwargs):
		user = request.user
		profile = Profile.objects.filter(user=user.id).first()
		image = None
		if profile.image:
			image = request.build_absolute_uri(profile.image.url)
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
			'short_description': profile.short_description,
			'image': image
		}

		return HttpResponse(
			json.dumps(jData),
			status=200,
			content_type="application/json"
		)

class ProfilePictureView(	mixins.CreateModelMixin,
							mixins.ListModelMixin,
							viewsets.GenericViewSet):
	"""
	API Endpoint that allows a user to update their photo
	"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	serializer_class = ProfilePictureSerializer

	def get_queryset(self):
		return Profile.objects.filter(user=self.request.user)

	def create(self, request, *args, **kwargs):
		user = Profile.objects.filter(user=request.user).first()
		user.image.delete()

		upload = request.data['file']

		user.image.save(upload.name, upload)
		serializer = self.get_serializer(Profile.objects.filter(user=request.user).first(), many=False)
		return Response(serializer.data, status=200)


class SearchView(ObjectMultipleModelAPIView):
	"""
	API endpoint for searching the database for useful information related to users.
	"""
	# authentication_classes = (TokenAuthentication,)
	# permission_classes = (IsAuthenticated,)

	def get_querylist(self):
		query = self.request.query_params['q']

		querylist = []

		unfiltered = User.objects.all()

		users = unfiltered.filter(email = query)
		users = users | unfiltered.filter(username__contains=query)
		users = users | unfiltered.filter(first_name__contains = query)

		if users.count() > 0:
			querylist.append({'queryset': users, 'serializer_class': UserSerializer})
		else:
			querylist.append({'queryset': User.objects.none(), 'serializer_class': UserSerializer})

		unfiltered = JobListing.objects.all()

		jobPosts = unfiltered.filter(job_email = query)
		jobPosts = jobPosts | unfiltered.filter(job_position__contains=query)
		jobPosts = jobPosts | unfiltered.filter(job_description__contains=query)

		if jobPosts.count() > 0:
			querylist.append({'queryset': jobPosts, 'serializer_class': JobPostSerializer})
		else:
			querylist.append({'queryset': JobListing.objects.none(), 'serializer_class': JobPostSerializer})

		availPosts = AvailabilityListing.objects.filter(description__contains=query)

		if availPosts.count() > 0:
			querylist.append({'queryset': availPosts, 'serializer_class': AvailabilityPostSerializer})
		else:
			querylist.append({'queryset': AvailabilityListing.objects.none(), 'serializer_class': AvailabilityPostSerializer})

		return querylist

class ApplicationView(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
	"""
	API endpoint that allows a user to be viewed with authentication
	1. Create a Superuser using the manage.py
	2. Create a User from the admin panel (If desired, not nessesarily required)
	3. Make a Post request to hostname/getUserJsonAuth/ with the following in the headers
	key = Authorization
	data = Token with your JWT from the login
	"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	serializer_class = ProfileSerializer
	
	def get_queryset(self):
		applications = Application.objects.filter(user=self.request.user)
		return applications.filter(job_listing=self.request.query_params.get('jobPost', None))

	def create(self, request):
		application = Application.objects.create(user=request.user, job_listing=JobListing.objects.filter(id=request.data['job_post']).first())

		profile = Profile.objects.filter(user=self.request.user).first()
		jData = {
			'id': int(profile.id),
			'username': str(profile.user.username),
			'first_name': str(profile.user.first_name),
			'last_name': str(profile.user.last_name),
			'email': str(profile.user.email),
			'Group': str(profile.user.groups),
			'zipcode': profile.zipcode,
			'rating':profile.rating,
			'skills': profile.skills,
			'short_description': profile.short_description
		}

		returnApplications = []
		app = {}
		app['job_post'] = application.job_listing.id 
		app['user'] = jData
		returnApplications.append(app)

		return HttpResponse(
			json.dumps(returnApplications),
			status=201,
			content_type="application/json"
		)

	def list(self, request):
		queryset = Application.objects.filter(user=self.request.user)
		applications = queryset.filter(job_listing=self.request.query_params.get('jobPost', None))
		profile = Profile.objects.filter(user=self.request.user).first()
		jData = {
			'id': int(profile.id),
			'username': str(profile.user.username),
			'first_name': str(profile.user.first_name),
			'last_name': str(profile.user.last_name),
			'email': str(profile.user.email),
			'Group': str(profile.user.groups),
			'zipcode': profile.zipcode,
			'rating':profile.rating,
			'skills': profile.skills,
			'short_description': profile.short_description
		}
		
		returnApplications = []
		for application in applications:
			app = {}
			app['job_post'] = application.job_listing.id 
			app['user'] = jData
			returnApplications.append(app)

		return HttpResponse(
			json.dumps(returnApplications),
			status=200,
			content_type="application/json"
		)
