# Project Import
from apps.courses.models import Courses, WhatYouLearn, AboutCourse, CareerPath, TheseCourseIsForYou, Syllabus, SubSyllabus

# Third Party Import
from rest_framework import serializers


class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = [
            "id",
            "course_name",
            "description",
            "course_image"
        ]


class WhatYouLearnSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()

    class Meta:
        model = WhatYouLearn
        fields = [
            "id",
            "course_name",
            "whatyoulearn_description",
        ]

    def get_course_name(self, obj):
        return obj.course_name.course_name


class AboutCourseSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()

    class Meta:
        model = AboutCourse
        fields = [
            "course_name",
            "aboutcourse_description",
        ]

    def get_course_name(self, obj):
        return obj.course_name.course_name


class CareerPathSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()

    class Meta:
        model = CareerPath
        fields = [
            "course_name",
            "career_path_description",
        ]

    def get_course_name(self, obj):
        return obj.course_name.course_name


class TheseCourseIsForYouSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()

    class Meta:
        model = TheseCourseIsForYou
        fields = [
            "course_name",
            "description",
        ]

    def get_course_name(self, obj):
        return obj.course_name.course_name
    

class SyllabusSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()

    class Meta:
        model = Syllabus
        fields = [
            "course_name",
            "chapter",
            "chapter_description",
        ]

    def get_course_name(self, obj):
        return obj.course_name.course_name


class SubSyllabusSerializer(serializers.ModelSerializer):
    # course_name = serializers.SerializerMethodField()
    # chapter = serializers.SerializerMethodField()
    class Meta:
        model = SubSyllabus
        fields = [
            "syllabus",
            "sub_chapter",
            "subchapter_description",
            "sub_syllabus_image",
        ]
