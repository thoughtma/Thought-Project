
# Django Import 
from django.urls import path

# Project Import 
from apps.trainer import views


urlpatterns = [
    path("trainer/create/", views.TrainerCreateApiView.as_view()),
    path(
        "trainer/retrive/<int:id>/", views.TrainerRetriveApiView.as_view()
    ),
]
