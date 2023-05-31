# Django Import
from django.urls import path
from .views import *


urlpatterns = [
    # Admin url
    path('', admin_login, name='admin_login'),
    path('dashboard/', admin_dashboard, name='dashboard'),
    path('logout/', admin_logout, name='admin_logout'),
    # path('dashboard/',admin_dashboard, name='dashboard'),
    path('test/',admin_test, name='test'),

    # Users url
    path('users/',all_users, name='users'),
    path('user-detail-view/<int:id>/',user_detail_view, name='user_detail_view'),
    path('users/update/<int:id>/',user_update, name='user_update'),
    path('users/change/status/<int:id>/', change_user_status, name='change-user-status'),
    path('user-delete/<int:id>/', user_delete, name = "user-delete"),

    # Cources url
    path('courses/',courses, name='courses'),
    path('courses/add-course',add_course, name='add-course'),
    path('courses/update/<int:id>/', course_update, name='course_update'),
    path('courses/delete/<int:id>/', course_delete, name='course_delete'),
    path('courses/<int:id>/', course_detail, name='course_detail'),
    path('courses/deactivate/<int:id>/', course_changestatus, name='deactivate-course'),

    # What you learn url
    path('whatyoulearn/',whatyoulearn, name='whatyoulearn'),
    path('whatyoulearn/update/<int:id>/', whatyoulearn_update, name='whatyoulearn_update'),
    path('whatyoulearn/delete/<int:id>/', whatyoulearn_delete, name='whatyoulearn_delete'),
    path('whatyoulearn/<int:id>/', whatyoulearn_detail, name='whatyoulearn_detail'),

    # About course url
    path('about-course/',aboutcourse, name='aboutcourse'),
    path('about-course/update/<int:id>/', aboutcourse_update, name='aboutcourse_update'),
    path('about-course/delete/<int:id>/', aboutcourse_delete, name='aboutcourse_delete'),
    path('about-course/<int:id>/', aboutcourse_detail, name='aboutcourse_detail'),

    # Career path url
    path('career-path/',career_path, name='career_path'),
    path('career-path/<int:id>/', career_path_detail, name='career_path_detail'),
    path('career-path/update/<int:id>/', career_path_update, name='career_path_update'),
    path('career-path/delete/<int:id>/', career_path_delete, name='career_path_delete'),

    # Syllabus url
    path('syllabus/',syllabus, name='syllabus'),
    path('syllabus/<int:id>/',syllabus_detail, name='syllabus_detail'),
    path('syllabus/update/<int:id>/',syllabus_update , name='syllabus_update'),
    path('syllabus/delete/<int:id>/',syllabus_delete , name='syllabus_delete'),
    path('syllabus/deactivate/<int:id>/', syllabus_changestatus, name='deactivate-syllabus'),


    # Subsyllabus url
    path('subsyllabus/',subsyllabus, name='subsyllabus'),
    path('subsyllabus/<int:id>/', subsyllabus_detail, name='subsyllabus_detail'),
    path('subsyllabus/update/<int:id>/', subsyllabus_update, name='subsyllabus_update'),
    path('subsyllabus/delete/<int:id>/', subsyllabus_delete, name='subsyllabus_delete'),
    path('subsyllabus/deactivate/<int:id>/', subsyllabus_changestatus, name='deactivate-subsyllabus'),


    # Student url
    path('students/',student, name='add-student'),
    path('update-student/<int:id>',student_update, name='update-student'),
    path('student-detail-view/<int:id>',student_detail_view, name='student_detail_view'),
    path('student/delete/<int:id>/', student_delete, name='student-delete' ),
    path('student/deactivate/<int:myid>/', changestatus, name='deactivate-student'),

    # # Trainer url
    # path('trainers/', all_trainer, name='trainer'),
    # path('trainer-detail-view/',trainer_detail_view, name='trainer_detail_view'),

    #Trainer url
    path('trainer/', all_trainer, name='trainer'),
    path('trainer-detail-view/<int:id>/',trainer_detail_view, name='trainer-detail-view'),
    path('trainer/update/<int:id>/', trainer_update, name='trainer-update'),
    path('trainer/delete/<int:id>/', trainer_delete, name='trainer-delete'),
    path('trainer/deactivate/<int:id>/', trainer_changestatus, name='deactivate-trainer'),
    path('check_email/<str:eamil>/', check_email, name='check_email'),
    #Lecturevideo Url
    path('trainer/lecturevideo/', trainer_lecturevideo, name='trainer-lecturevideo'),
    path('lecture-video/<int:pk>/', trainer_play_lecture_video, name='play_video'),
    path('trainer-lecturevideo-detail-view/<int:id>/',trainer_lecturevideo_detail_view, name='lecturevideo-detail-view'),
    path('trainer/lecturevideo/delete/<int:id>/', trainer_lecturevideo_delete, name='trainer-lecturevideo-delete'),
    path('trainer/lecturevideo/update/<int:id>/', trainer_lecturevideo_update, name='trainer-lecturevideo-update'),

    #Quries Url
    # path('trainer/query/', add_show_quires, name='trainer-quires'),
    # path('trainer/query/detail/<int:id>/',query_detail_view, name='query-view'),
    path('trainer/query/delete/<int:id>/', query_delete, name='query-delete'),
    # path('trainer/query/update/<int:id>/', query_update, name='query-update'),
    path('all_queries/', show_queries, name='show-queries' ),
    # path('query-detail-view/<int:query_id>/', query_detail, name='query_detail'),
    # path('query/<int:query_id>/', query_detail, name='query_detail'),
    path('query-detail/<int:query_id>/',query_detail, name='query_detail'),

    # Contact US urls
    path('contactforms/',contact_forms, name='contactforms'),
    path('contactforms/<int:id>/', contact_form_detail, name='contactforms_detail'),
    path('contactforms/delete/<int:id>/', contact_form_delete, name='contactforms_delete'),

    # Enquiry Forms urls
    path('enquiryforms/',enquiry_forms, name='enquiryforms'),
    path('enquiryforms/<int:id>/', enquiry_form_detail, name='enquiryforms_detail'),
    path('enquiryforms/update/<int:id>/', enquiry_form_update, name='enquiryforms_update'),
    path('enquiryforms/delete/<int:id>/', enquiry_form_delete, name='enquiryforms_delete'),

    # Review Forms urls
    path('reviewforms/',review_forms, name='reviewforms'),
    path('reviewforms/<int:id>/', review_form_detail, name='reviewforms_detail'),
    path('reviewforms/delete/<int:id>/', review_form_delete, name='reviewforms_delete'),

    # Profile urls
    path('profile/',profile, name='user_profile'),
    path('changepassword/',change_password, name='change_password'),

    # PDF Invoice generate
    path('invoice/', generate_invoice, name='invoice'),

    # Test Papers Questions URLs
    path('questions/list/', create_question, name='questions-create'),
    path('questions/list/<int:id>/', question_detail, name='questions-detail'),
    path('questions/list/update/<int:id>/', question_update, name='question_update'),
    path('questions/list/delete/<int:id>/', question_delete, name='question_delete'),
]
