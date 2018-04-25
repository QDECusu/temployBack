#For Authentication
from rest_framework import status, exceptions
from django.http import HttpResponse
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from django.contrib.auth.models import User
from django.conf import settings
import jwt
import json

class TokenAuthentication(BaseAuthentication):

	model = None

	def get_model(self):
		return User

	#Verifies that the token is valid before passing it on to authenticate_credentials
	def authenticate(self, request):
		auth = get_authorization_header(request).split()
		if not auth or auth[0].lower() != b'token':
			return None

		if len(auth) == 1:
			msg = 'Invalid token header. No credentials provided.'
			raise exceptions.AuthenticationFailed(msg)
		elif len(auth) > 2:
			msg = 'Invalid token header'
			raise exceptions.AuthenticationFailed(msg)

		try:
			token = auth[1]
			if token=="null":
				msg = 'Null token not allowed'
				raise exceptions.AuthenticationFailed(msg)
		except UnicodeError:
			msg = 'Invalid token header. Token string should not contain invalid characters.'
			raise exceptions.AuthenticationFailed(msg)

		return self.authenticate_credentials(token)

	#Validates JWT
	def authenticate_credentials(self, token):
		model = self.get_model()
		payload = jwt.decode(token, settings.SECRET_KEY)
		username = payload['username']
		userid = payload['id']
		msg = {'Error': "Token mismatch",'status' :"401"}
		try:
			
			user = User.objects.get(
				username=username,
				id=userid,
				is_active=True
			)

			return (user, token)

		#TODO Need to get this portion below working, but it works for now, just doesn't do all validation			
			if not user.token['Token'] == token:
				raise exceptions.AuthenticationFailed(msg)
			   
		except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:
			return HttpResponse({'Error': "Token is invalid"}, status="403")
		except User.DoesNotExist:
			return HttpResponse({'Error': "Internal server error"}, status="500")

		return (user, token)

	def authenticate_header(self, request):
		return 'Token'