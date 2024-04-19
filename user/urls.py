from django.urls import path

from . import views

urlpatterns = [
    path('register', views.RegistrationView.as_view(), name='register'),
    path('activate/<surl>', views.reset_password, name='activate'),
    path('forgot_password', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset_password/<surl>', views.reset_password, name='reset_password'),
    path('change_password/<user_id>', views.ChangePasswordView.as_view(), name='change_password'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.user_logout, name='logout')
 ]