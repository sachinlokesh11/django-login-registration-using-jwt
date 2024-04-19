from django.urls import path

from . import views

urlpatterns = [
    path('register', views.RegistrationView.as_view(), name='register'),
    path('reset_password/<surl>', views.reset_password, name='reset_password'),
    path('logout', views._logout, name='logout')
 ]