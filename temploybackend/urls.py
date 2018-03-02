from TemployProj.urls import path
from django.conf.urls import url
from . import views, auth


#django rest framework stuff
from django.conf.urls import url, include
from rest_framework import routers

#Django Rest routes
router = routers.DefaultRouter()
router.register(r'userView', views.TestUserViewNoAuth)
router.register(r'userViewAuth', views.TestAuth)
#router.register(r'getPosts', views.getPosts, base_name='post-list')
###########################

urlpatterns = [
	url(r'^', include(router.urls)),
	url(r'^api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('home/', views.Home.as_view(), name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('getAllUsersNonAuth/', views.TestSimpleUserJson.as_view(), name='getAllUsersNonAuth'),
	path('getUserDetail/', views.TestSimpleUserJsonAuth.as_view(), name='getUserDetail'),
	path('getPosts/', views.getPosts.as_view(), name='getPosts'),
	url(r'signup/', views.CreateUserView.as_view(), name='signup')
]