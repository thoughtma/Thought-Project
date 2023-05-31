# Django Import
from django.contrib import admin

# Project Import
from .models import Trainer, LectureVideo, Queries, ReplyThread


class TrainerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','email', 'contact', 'specialization', 'experience', 'address', 'is_active']
admin.site.register(Trainer, TrainerAdmin)


class LectureVideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'trainer', 'syllabus', 'title', 'lecture_video']
admin.site.register(LectureVideo, LectureVideoAdmin)


# class QueriesAdmin(admin.ModelAdmin):
#     list_display = ['id', 'student', 'syllabus', 'query_headline', 'query', 'response', 'response_by']

admin.site.register(Queries)


  
admin.site.register(ReplyThread)