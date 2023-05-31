# DJango Import
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Project Import
from apps.accounts.models import User
from apps.trainer.models import Trainer, LectureVideo, Queries

# Thgird Party Import
from rest_framework import serializers


class TrainerSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    email = serializers.SerializerMethodField()
    # first_name = serializers.SerializerMethodField()
    # last_name = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    contact = serializers.SerializerMethodField()
    password = serializers.SerializerMethodField()
    # profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = Trainer
        fields = [
            "id",
            # "first_name",
            # "last_name",
            "name",
            "email",
            "contact",
            "password",
            # "user_type",
            # "profile_pic",
            "specialization",
            "experience",
            "address"
        ]

    def get_id(self, obj):
        return obj.user.id
    
    def get_email(self, obj):
        return obj.user.email

    # def get_first_name(self, obj):
    #     return obj.user.first_name

    # def get_last_name(self, obj):
    #     return obj.user.last_name

    def get_name(self, obj):
        return obj.user.name
    
    def get_contact(self, obj):
        return obj.user.contact

    def get_password(self, obj):
        return obj.user.password

    # def get_profile_pic(self, obj):
    #     if obj.user.profile_pic:
    #         return settings.BACKEND_URL + obj.user.profile_pic.url
    #     else:
    #         return None


class LectureVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureVideo
        fields = [
            "course", 
            "trainer", 
            "syllabus", 
            "title", 
            "lecture_video"
            ]


class QueriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queries
        fields = [
            "student", 
            "syllabus", 
            "query_headline", 
            "query", 
            "response", 
            "response_by"
            ]