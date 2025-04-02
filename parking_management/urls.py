from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('spaces/', views.spaces_list , name = 'spaces_list'),
    path('booking/', views.add_booking , name = 'booking'),
    path('assign/', views.assign , name = 'assign'),
    path('unlock/', views.unlock , name = 'unlock'),
    path('cancel/', views.cancel , name = 'cancel'),
    path('logout/', views.logout , name = 'logout'),
]