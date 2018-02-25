from TemployProj.urls import path
from django.conf.urls import url
from . import views, auth

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('login/', views.Login.as_view(), name='login'),
]