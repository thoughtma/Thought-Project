# Django Import
from django.urls import path

# Project Import 
from apps.common import views


urlpatterns = [
    path('pycompiler/', views.RunCode.as_view(), name='pycompiler'),
    path('offices/', views.OurOfficesApiView.as_view()),
    path('subscribe/', views.SubscribeAPIView.as_view(), name='subscribe'),
    # path('notifications/', NotificationView.as_view(), name='notifications'),

    path('', views.index, name="indexpage"),
    path('runcode/', views.runcode, name="runcode"),
]
