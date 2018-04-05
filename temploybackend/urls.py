from TemployProj.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views, auth, JobPosts, AvailabilityPost


#django rest framework stuff
from django.conf.urls import url, include
from rest_framework import routers

#Django Rest routes
router = routers.DefaultRouter()
router.register(r'userView', views.TestUserViewNoAuth)
router.register(r'userViewAuth', views.TestAuth)
router.register(r'JobPosts', JobPosts.jobPostViewSet, base_name="JobPosts")
router.register(r'AvailabilityPosts', AvailabilityPost.availabilityPostViewSet, base_name="AvailabilityPosts")
router.register(r'Profile', views.ProfileView, base_name="Profile")
#router.register(r'search', views.SearchView, base_name='search')
###########################

urlpatterns = [
	url(r'^', include(router.urls)),
	url(r'^api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('home/', views.Home.as_view(), name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('getAllUsersNonAuth/', views.TestSimpleUserJson.as_view(), name='getAllUsersNonAuth'),
	path('getUserDetail/', views.TestSimpleUserJsonAuth.as_view(), name='getUserDetail'),
	path('search', views.SearchView.as_view(), name='search'),
	path('listUserJobPosts/', JobPosts.getUserPostView.as_view(), name='listUserJobPosts'),
	path('listUserAvailabilityPosts/', JobPosts.getUserPostView.as_view(), name='listUserAvailabilityPosts'),	
	path('profileDetail/', views.UserProfileView.as_view(), name='profileDetail'),
	url(r'signup/', views.CreateUserView.as_view(), name='signup'),
]