# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

# Project Imports
from apps.accounts.models import BaseModel
# from apps.trainer.models import Trainer
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone


class Courses(BaseModel):
    COURSE_CATEGORY = (
        ("PYTHON IT", "Python IT"),
        ("REACTJS IT", "ReactJS IT"),
        ("QA IT", "QA IT"),
        ("PYTHON NON-IT", "Python NON-IT"),
        ("REACTJS NON-IT", "ReactJS NON-IT"),
        ("QA NON-IT", "QA NON-IT"),
    )
    CATEGORY_CHOICES = [
        ('IT', 'IT'),
        ('NON-IT', 'Non-IT'),
    ]
    course_name = models.CharField(
        max_length=100,
        choices=COURSE_CATEGORY,
        null=True,
        blank=True,
    )
    title = RichTextUploadingField(blank = True,default="Python")
    description = RichTextUploadingField(blank = True,default="Description about courses")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=Decimal('0.0'))
    students_enrolled = models.PositiveIntegerField(default=0)
    job_guarantee = models.CharField(max_length=100,blank= True)
    online_classes = models.CharField(max_length=100, blank= True)
    offline_classes = models.CharField(max_length=100,blank= True)
    duration = models.CharField(max_length= 50,blank= True)
    skills = models.CharField(max_length= 200,blank= True)
    start_date = models.DateField(default=timezone.now)
    language = models.CharField(max_length=100,blank= True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES,default="IT")
    course_image = models.ImageField(
        upload_to='media/courses/', null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.course_name}'

class WhatYouLearn(BaseModel):
    # module_name = models.CharField(max_length=100, null=True, blank=True)
    course_name = models.ForeignKey(
        Courses,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    whatyoulearn_description = RichTextUploadingField(blank = True,default="whatyoulearn_description")

    def __str__(self):
        return f"{self.course_name}"


class AboutCourse(BaseModel):
    course_name = models.ForeignKey(
        Courses,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    aboutcourse_description = RichTextUploadingField(blank = True,default="aboutcourse_description")
    about_course_image = models.ImageField(
        upload_to='media/courses/about_course_image/', null=True, blank=True)

    def __str__(self):
        return f"{self.course_name}"


class CareerPath(models.Model):
    course_name = models.ForeignKey(
        Courses,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    career_path_description = RichTextUploadingField(blank = True,default="career_path_description")
    career_path_image = models.ImageField(
        upload_to='media/courses/career_path_image/', null=True, blank=True)

    def __str__(self):
        return f"{self.course_name}"


class TheseCourseIsForYou(models.Model):
    course_name = models.ForeignKey(
        Courses,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    description = RichTextUploadingField(default="TheseCourseIsForYou About")
    specification = models.TextField(blank=True, null=True)


class Syllabus(models.Model):
    course_name = models.ForeignKey(
        Courses,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    chapter = models.CharField(max_length=300, null=True, blank=True)
    chapter_description = RichTextUploadingField(blank = True,default = "description")
    syllabus_image = models.ImageField(
        upload_to='media/courses/syllabus_image/', null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.course_name}  {self.chapter}"


class SubSyllabus(models.Model):
    syllabus = models.ForeignKey(
        Syllabus,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    sub_chapter = RichTextUploadingField(blank= True,default = "description")
    subchapter_description = RichTextUploadingField(blank= True,default = "description")
    sub_syllabus_image = models.ImageField(
        upload_to='media/courses/sub_syllabus_image/', null=True, blank=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.sub_chapter}"
