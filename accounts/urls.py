from django.urls import path
from . import views
from django.contrib.auth.views import login, logout
urlpatterns = [
	path('',views.dashboardView, name='home'),
	path('login/',login,name='login'),
	path('profile/',views.profile, name='profile'),
	path('register/',views.registerView, name='register'),
	path('logout/',logout, name="logout"),
]