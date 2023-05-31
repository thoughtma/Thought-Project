# Django Import
from django.contrib import admin

# Project Import
from .models import Courses, WhatYouLearn, AboutCourse, CareerPath, TheseCourseIsForYou, Syllabus, SubSyllabus


class CoursesAdmin(admin.ModelAdmin):
    list_display = ['id', 'course_name', 'title',
                    'description','students_enrolled','job_guarantee','online_classes','offline_classes','duration','skills','start_date','language','category','rating','course_image']


admin.site.register(Courses, CoursesAdmin)


class WhatYouLearnAdmin(admin.ModelAdmin):
    list_display = ['id', 'course_name', 'whatyoulearn_description']


admin.site.register(WhatYouLearn, WhatYouLearnAdmin)


class AboutCourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'course_name',
                    'aboutcourse_description', 'about_course_image']


admin.site.register(AboutCourse, AboutCourseAdmin)


class CareerPathAdmin(admin.ModelAdmin):
    list_display = ['id', 'course_name', 'career_path_description', 'career_path_image']


admin.site.register(CareerPath, CareerPathAdmin)


class TheseCourseIsForYouAdmin(admin.ModelAdmin):
    list_display = ['id', 'course_name', 'description', 'specification']


admin.site.register(TheseCourseIsForYou, TheseCourseIsForYouAdmin)


class SyllabusAdmin(admin.ModelAdmin):
    list_display = ['id', 'course_name', 'chapter',
                    'chapter_description', 'syllabus_image']


admin.site.register(Syllabus, SyllabusAdmin)


class SubSyllabusAdmin(admin.ModelAdmin):
    list_display = ['id', 'syllabus', 'sub_chapter',
                    'subchapter_description', 'sub_syllabus_image']


admin.site.register(SubSyllabus, SubSyllabusAdmin)
