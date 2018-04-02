from django.http import HttpResponse
#For login portion
import jwt, json
from rest_framework import views
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
from .serializers import UserSerializer, GroupSerializer, JobPostSerializer, CreateUserSerializer, ProfileSerializer
from .models import JobListing, Profile
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

		return HttpResponse(
			json.dumps(jData),
			status=200,
			content_type="application/json"
		)

# class SearchView(generics.ListAPIView):
#     """
#     Will search users, job posts, availability listings*TBA
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (IsAdminUser,)

#     def list(self, request):
#         # Note the use of `get_queryset()` instead of `self.queryset`
#         queryset = self.get_queryset()
#         serializer = UserSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def get_queryset(self):
#         result = super(SearchView, self).get_queryset()

#         query = self.request.GET.get('q')
#         if query:
#             query_list = query.split()
#             result = result.filter(
#                 reduce(operator.and_,
#                        (Q(title__icontains=q) for q in query_list)) |
#                 reduce(operator.and_,
#                        (Q(content__icontains=q) for q in query_list))
#             )

#         return result

class SearchView(views.APIView):
        """
        API endpoint that allows a user to be viewed with authentication, and outputs the authed user
        1. Create a Superuser using the manage.py
        2. Create a User from the admin panel (If desired, not nessesarily required)
        3. Make a Post request to hostname/getUserJsonAuth/ with the following in the headers
        key = Authorization
        data = Token with your JWT from the login
        """
        # authentication_classes = (TokenAuthentication,)
        # permission_classes = (IsAuthenticated,)

        def get(self, request, *args, **kwargs):
                request = request.query_params['q']

                users = User.objects.filter(username__icontains=request)

                reduce(operator.and_,)

                jData = {
                        'postData': str(request)
                }

                return HttpResponse(
                        json.dumps(jData),
                        status=200,
                        content_type="application/json"
                )
