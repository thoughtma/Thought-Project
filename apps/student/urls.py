# Django Import
from django.urls import path

# Project Import
from apps.student import views


urlpatterns = [
     
     # Enquery Form URL
     path("student/create/", views.StudentCreateApiView.as_view() ,name='add-student'),
     path("enqueryform/create/", views.EnquirersFormsCreateApiView.as_view()),
     path("contactform/create/", views.ContactFormApiView.as_view()),

     # Student Accounts URL
     path("student_review/create/", views.StudentReviewListCreateView.as_view()),
     path('student_review/<int:pk>/', views.StudentReviewRetrieveUpdateDestroyAPIView.as_view()),
     path("student/profile/<int:user_id>/", views.StudentProfileCreateApiView.as_view() ,name='student-profile'),
     path("mycourse/", views.StudentCourseDetails.as_view()),
     path("mycourse/details/<int:course_id>/", views.MyCourseDetails.as_view()),
     path("certificate/", views.StudentCertificateApiView.as_view()),

     # Student Queries URL
     path("queries/", views.CreateRetriveAllQuery.as_view()),
     path("create-reply/", views.CreateReplyAPIView.as_view()),
     path("reply/<int:reply_id>", views.RetriveAllReplyAPIView.as_view()),
     path("fake/enty/delete/", views.FakeEntryDelete.as_view()),

     # Students Course Details
     path("course/details/<int:course_id>/", views.StudentCourseDetailsAPI.as_view()),
     path("course/modules/<int:course_id>/", views.StudentCourseModuleAPIView.as_view()),
     path("course/modules/details/<int:syallbus_id>/", views.StudentCourseModuleDetailsAPIView.as_view()),

     # Revision Test
     path("test/revision/<int:course_id>/<int:syllabus_id>/", views.RevisionTest.as_view()),
     path("test/practice/<int:course_id>/<int:syllabus_id>/", views.PracticeTest.as_view()),
     

]
