# Django Import
from django.urls import path

# Project Import
from .views import (
    CourseListCreateApiView,
    CourseRetrieveAPIView,
    WhatYouLearnRetrieveApiView,
    AboutCourseRetrieveAPIView,
    CareerPathRetrieveApiView,
    TheseCourseIsForYouRetrieveApiView,
    SyllabusRetrieveApiView,
    SubSyllabusRetrieveUpdateDestroyApiView,
)


urlpatterns = [
    # Courses URLs
    path('courses/', CourseListCreateApiView.as_view()),
    path('courses/<int:pk>/', CourseRetrieveAPIView.as_view()),

    # WhatYouLearn URLs
    path('whatyoulearn/<int:user_course_id>/',
         WhatYouLearnRetrieveApiView.as_view()),

    # AboutCourse URLs
    path('aboutcourse/<int:user_course_id>/', AboutCourseRetrieveAPIView.as_view()),

    # CareerPath URLs
    path('careerpath/<int:user_course_id>/', CareerPathRetrieveApiView.as_view()),

    # These Course Is For You URLs
    path('these-course-is-for-you/<int:user_course_id>/', TheseCourseIsForYouRetrieveApiView.as_view()),

    # Syllabus URLs
    path('syllabus/<int:user_course_id>/', SyllabusRetrieveApiView.as_view()),

    # SubSyllabus URLs
    path('subsyllabus/<int:pk>/', SubSyllabusRetrieveUpdateDestroyApiView.as_view()),
]
