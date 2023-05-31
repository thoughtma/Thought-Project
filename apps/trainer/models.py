
# Django Imports
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

# Project Imports
from apps.accounts.models import BaseModel, User
from apps.courses.models import Courses, Syllabus
from apps.student.models import Student

class Trainer(BaseModel):
    COURSE_CATEGORY = (
        ("PYTHON", "Python"),
        ("REACTJS", "ReactJS"),
        ("QA", "Qa"),
    )
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True)
    contact = models.IntegerField()
    specialization = models.CharField(
        max_length=100,
        choices=COURSE_CATEGORY
    )
    experience = models.FloatField()
    address = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.name)


class LectureVideo(models.Model):
    course = models.ForeignKey(
        Courses,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    trainer = models.ForeignKey(
        Trainer,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    syllabus = models.ForeignKey(
        Syllabus,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    lecture_video = models.FileField(
        upload_to='media/trainer/lecture_video/', null=True, blank=True)

    def __str__(self):
        return self.title

class Queries(models.Model):
    student = models.ForeignKey(
        Student,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    headline = models.TextField(blank=True)
    query = models.TextField(blank=True)
    is_resolved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student} | {self.query}"
    
@receiver(post_save, sender=Queries)
def create_profile(sender, instance, created, **kwargs):
    if created:
        ReplyThread.objects.create(queries=instance,query = instance.query)
    

class ReplyThread(models.Model):
    queries = models.ForeignKey(
        Queries,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
   
    query = models.TextField(blank=True)
    response = models.TextField(blank=True)
    response_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    
    def __str__(self) -> str:
        return f'{self.queries}'