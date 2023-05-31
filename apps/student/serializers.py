
# Project Import
from apps.student.models import Student, StudentReviews, EnquirersForms, ContactForms, Question, Answer, RevisionTest
from apps.accounts.models import User
from apps.student.models import Student, StudentReviews, EnquirersForms, ContactForms, Certificate
from apps.student.models import Courses, UserCourse , UserCourseModule
from apps.courses.serializers import CoursesSerializer
from apps.trainer.models import Queries, ReplyThread
from apps.courses.models import SubSyllabus, Syllabus

# Third Party Import
from rest_framework import serializers

# Dajngo Import
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re


class StudentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    email = serializers.SerializerMethodField()
    # first_name = serializers.SerializerMethodField()
    # last_name = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    contact = serializers.SerializerMethodField()
    password = serializers.SerializerMethodField()
    # profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = Student
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
            "highest_qualification",
            "category",
            "local_address",
            "permanent_address",
            "father_name",
            "father_mobile_number",
            "enrolled_course",
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


class StudentReviewsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    course_detail = serializers.SerializerMethodField()

    class Meta:
        model = StudentReviews
        fields = [
            'id',
            'student',
            'user',
            'course',
            'course_detail',
            'rating',
            'comment',

        ]
        # read_only_fields = ['id', 'student']

    def get_user(self, obj):
        return obj.student.user.name

    def get_course_detail(self, obj):
        return obj.course.course_name


class EnquirersFormsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnquirersForms
        fields = [
            "name",
            "mobile_number",
            "email",
            "highest_qualification",
            "category"
        ]

    def validate_name(self, value):
        
        if not value.isalpha():
            raise serializers.ValidationError("Name should only contain letters.")
        
        max_length = 30
        if len(value) > max_length:
            raise serializers.ValidationError(f"Name cannot exceed {max_length} characters.")
        return value
    
    def validate_mobile_number(self, value):
        
        if not value.isdigit():
            raise serializers.ValidationError("Mobile number should only contain digits.")
        
        max_length = 10
        if len(value) > max_length:
            raise serializers.ValidationError(f"Mobile number cannot exceed {max_length} digits.")
        return value
    

    def validate_email(self, value):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Invalid email address.")
        if not value.endswith('.com'):
            raise serializers.ValidationError("email must have .com domain.")

        return value
    
    


class ContactFormsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForms
        fields = [
            "name",
            "contact",
            "email",
            "message"
        ]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "name", "contact", "email", "profile_pic"]


class StudentProfileSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    email = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    contact = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            "id",
            "name",
            "email",
            "contact",
            "profile_pic",
            "highest_qualification",
            "category",
            "permanent_address",
        ]

    def get_id(self, obj):
        return obj.user.id

    def get_email(self, obj):
        return obj.user.email

    def get_name(self, obj):
        return obj.user.name

    def get_contact(self, obj):
        return obj.user.contact

    def get_profile_pic(self, obj):
        if obj.user.profile_pic:
            return self.context['request'].build_absolute_uri(obj.user.profile_pic.url)
        else:
            return None


class StudentCourseSerializer(serializers.ModelSerializer):
    enrolled_course = CoursesSerializer(many=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "enrolled_course"
        ]

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'
        depth = 1


class QueriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queries
        fields = ['id', 'student', 'headline','query']


class QueriesReplySerializer(serializers.ModelSerializer):
    queries = QueriesSerializer()
    class Meta:
        model = ReplyThread
        fields = [ 'queries', 'query', 'response']


class QueriesReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyThread
        fields = [ 'queries', 'query', 'response']



class ReplyThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyThread
        fields = ['query', 'response']



class CoursesSerializerDetails(serializers.ModelSerializer):
    course_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Courses
        fields = [
            "id",
            "course_name",
            "description",
            'course_image'
        ]
   
    def get_course_image(self, obj):
        if obj.course_image:
            return self.context['request'].build_absolute_uri(obj.course_image.url)
        else:
            return None


class StudentCourseDetailSerializer(serializers.ModelSerializer):
    course_name = CoursesSerializerDetails()

    class Meta:
        model = UserCourse
        fields = ['id','course_name']



class SyllabusDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Syllabus
        fields = [
            "id",
            "chapter",
            "chapter_description",
        ]



class CoursesDetailSerializerDetails(serializers.ModelSerializer):
    course_image = serializers.SerializerMethodField()

    class Meta:
        model = Courses
        fields = ['id', 'course_name', 'title',
                    'description','students_enrolled','job_guarantee','online_classes',
                    'offline_classes','duration','skills','start_date','language','category','rating','course_image']
    

    def get_course_image(self, obj):
        if obj.course_image:
            return self.context['request'].build_absolute_uri(obj.course_image.url)
        else:
            return None



class StudentCourseDetailsSerializer(serializers.ModelSerializer):
    course_name = CoursesDetailSerializerDetails()

    class Meta:
        model = UserCourse
        fields = ['id','course_name']



class StudentCourseModuleSerializer(serializers.ModelSerializer):
    syllabus = SyllabusDetailsSerializer()

    class Meta:
        model = UserCourseModule
        fields = ['syllabus','syllabus_status']



class StudentCourseModuleDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SubSyllabus
        fields = ['sub_chapter','subchapter_description']


class AnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk')
    text = serializers.CharField(source='choice_answer')

    class Meta:
        model = Answer
        fields = ('id', 'text', 'is_correct')


class QuestionSerializer(serializers.ModelSerializer):
    question = serializers.CharField(source='question_title')
    options = AnswerSerializer(source='answers', many=True)

    class Meta:
        model = Question
        fields = ('id', 'test_type', 'question_type', 'question', 'options')
