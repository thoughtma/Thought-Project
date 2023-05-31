# Django Import
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Project Import
from apps.accounts import views


urlpatterns = [
    path("login/", views.UserLoginApi.as_view(), name="user-login"),
    path("change/password/", views.ChangePassword.as_view()), 
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<token>/', views.ResetPasswordView.as_view(), name='reset-password'),
]



