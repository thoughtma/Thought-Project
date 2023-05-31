# Django Import
from django.contrib import admin

# Project Import
from apps.student.models import Student, StudentReviews, EnquirersForms, ContactForms , Certificate, UserCourse, UserCourseModule, Question, Answer, RevisionTest

class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'highest_qualification', 'category', 'local_address',
                    'permanent_address', 'father_name', 'father_mobile_number', 'enrolled_course_display']

    def enrolled_course_display(self, obj):
        return ", ".join([course.course_name for course in obj.enrolled_course.all()])
    enrolled_course_display.short_description = 'Enrolled Courses'

admin.site.register(Student, StudentAdmin)


class StudentReviewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'course', 'rating', 'comment']

class CertificateAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'course', 'title', 'description','certificate_file']


admin.site.register(Certificate, CertificateAdmin)

admin.site.register(StudentReviews, StudentReviewsAdmin)


class EnquirersFormsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'mobile_number',
                    'email', 'highest_qualification', 'category', 'comment' ,'priority']


admin.site.register(EnquirersForms, EnquirersFormsAdmin)


class ContactFormsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'contact', 'email', 'address', 'message']


admin.site.register(ContactForms, ContactFormsAdmin)

admin.site.register(UserCourse)
admin.site.register(UserCourseModule)



class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'test_type', 'question_title', 'question_type', 'is_active', 'course', 'syllabus', 'frequency']

admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'choice_answer', 'is_correct']
admin.site.register(Answer, AnswerAdmin)


class RevisionTestAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'syllabus', 'student', 'result']
    
admin.site.register(RevisionTest, RevisionTestAdmin)