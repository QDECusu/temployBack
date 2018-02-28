from django.http import HttpResponse
#For login portion
import jwt, json
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

#For Authenticating
from .auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#For django rest framework (+ serializers)
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins, generics
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer, GroupSerializer

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
			jwt_token = {'token': jwt.encode(payload, "SECRET_KEY").decode("utf-8") }

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
	serializer_class = UserSerializer