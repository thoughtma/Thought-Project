# Python Import
import logging

# Django Import
from django.shortcuts import get_object_or_404

# Project Import
from apps.accounts.models import User
from apps.student.models import Student, StudentReviews, EnquirersForms, ContactForms,Certificate, UserCourse, UserCourseModule, Question, Answer, RevisionTest
from apps.courses.models import Courses, SubSyllabus
from apps.trainer.models import Queries, ReplyThread
from apps.accounts.utils import create_student_user
from apps.accounts import create_response_util
from apps.student.serializers import (StudentSerializer, StudentReviewsSerializer, EnquirersFormsSerializer,
                                    ContactFormsSerializer,StudentProfileSerializer, StudentCourseSerializer, 
                                 CertificateSerializer, QueriesSerializer, QueriesReplySerializer, QueriesReplyCreateSerializer, ReplyThreadSerializer,
                                StudentCourseDetailSerializer, StudentCourseModuleDetailsSerializer, StudentCourseModuleSerializer, StudentCourseDetailsSerializer,QuestionSerializer )


# Third Party Import
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, generics


logger = logging.getLogger(__name__)
info_logger = logging.getLogger('info_logger')
exception_logger = logging.getLogger('exception_logger')
error_logger = logging.getLogger('error_logger')
warning_logger = logging.getLogger('warning_logger')


class StudentCreateApiView(generics.ListAPIView):
    serializer_class = StudentSerializer
    pagination_class = PageNumberPagination


    def get_queryset(self, *args, **kwargs):
        queryset = Student.objects.all()
        return queryset

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def list(self, request):
        try:
            student = self.get_queryset(request)
            students = self.paginate_queryset(student)
            serializer = self.serializer_class(students, many=True)
            pages = self.get_paginated_response(serializer.data)
            return create_response_util.create_response_data(
                message="success",
                status=status.HTTP_200_OK,
                data=pages.data,
                errors=None,
            )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )

    def post(self, request):
        try:
            data = request.data
            serializer = StudentSerializer(
                data=data, context={'request': request})
            if serializer.is_valid():
                user = create_student_user(request.data, "STUDENT")
                serializer.save(user=user)
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_200_OK,
                    data=serializer.data,
                    errors=None,
                )

            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_400_BAD_REQUEST,
                    data=None,
                    errors=serializer.errors,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )


class StudentReviewListCreateView(generics.ListCreateAPIView):
    """
    API view to list all reviews and create a new review
    """
    serializer_class = StudentReviewsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset = StudentReviews.objects.filter(student__user=self.request.user)
        return queryset

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset


    def list(self, request):
        try:
            studentreview = self.get_queryset(request)
            serializer = self.serializer_class(studentreview, many=True)
            return create_response_util.create_response_data(
                message="success",
                status=status.HTTP_200_OK,
                data=serializer.data,
                errors=None,
            )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )


    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            student = Student.objects.get(user=request.user)
            course_id = data.get('course')
            course = get_object_or_404(Courses, id=course_id)
            serializer = StudentReviewsSerializer(
                data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save(student=student, course=course)
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_200_OK,
                    data=serializer.data,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_400_BAD_REQUEST,
                    data=None,
                    errors=serializer.errors,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )

    

class StudentReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update and delete a specific StudentReview
    """
    serializer_class = StudentReviewsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = StudentReviews.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.check_object_permissions(request, instance)
            serializer = self.serializer_class(instance)
            return create_response_util.create_response_data(
                message="success",
                status=status.HTTP_200_OK,
                data=serializer.data,
                errors=None,
            )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )

    def get_queryset(self):
        queryset = StudentReviews.objects.filter(
            student__user=self.request.user)
        return queryset


    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.student.user != request.user:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_403_FORBIDDEN,
                    data=None,
                    errors="You are not authorized to update this review.",
                )
            serializer = StudentReviewsSerializer(
                instance, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_200_OK,
                    data=serializer.data,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_400_BAD_REQUEST,
                    data=None,
                    errors=serializer.errors,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.student.user != request.user:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_403_FORBIDDEN,
                    data=None,
                    errors="You are not authorized to delete this review.",
                )
            self.check_object_permissions(request, instance)
            instance.delete()
            return create_response_util.create_response_data(
                message="success",
                status=status.HTTP_200_OK,
                data=None,
                errors=None,
            )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )


class EnquirersFormsCreateApiView(generics.CreateAPIView):
    serializer_class = EnquirersFormsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = EnquirersForms.objects.all()
        return queryset

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            email = data.get('email')
            if email and EnquirersForms.objects.filter(email=email).exists():
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_400_BAD_REQUEST,
                    data=None,
                    errors={'email': 'Email already exists.'},
                )
            serializer = EnquirersFormsSerializer(
                data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_201_CREATED,
                    data=serializer.data,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_400_BAD_REQUEST,
                    data=None,
                    errors=serializer.errors,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )


class ContactFormApiView(generics.ListCreateAPIView):
    serializer_class = ContactFormsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = ContactForms.objects.all()
        return queryset

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = ContactFormsSerializer(
                data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_201_CREATED,
                    data=serializer.data,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_400_BAD_REQUEST,
                    data=None,
                    errors=serializer.errors,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )


class StudentProfileCreateApiView(APIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        try:
            student = Student.objects.filter(user__id=user_id).last()
            if student:
                serializer = self.serializer_class(student, context = {'request' : request})
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_200_OK,
                    data=serializer.data,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_404_NOT_FOUND,
                    data=None,
                    errors=None,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )

    def put(self, request, user_id):
        try:
            student = Student.objects.filter(user__id=user_id).last()
            if student:
                user=student.user
                user.name = request.data.get('name', user.name)
                user.email = request.data.get('email', user.email)
                user.contact = request.data.get('contact', user.contact)
                user.profile_pic = request.data.get('profile_pic', user.profile_pic)
                user.save()
                serializer = self.serializer_class(student, data=request.data, partial=True, context = {'request' : request})

                if serializer.is_valid():
                    serializer.save()
                    return create_response_util.create_response_data(
                        message="success",
                        status=status.HTTP_200_OK,
                        data=serializer.data,
                        errors=None,
                    )
                else:
                    return create_response_util.create_response_data(
                        message="failed",
                        status=status.HTTP_400_BAD_REQUEST,
                        data=None,
                        errors=serializer.errors,
                    )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_404_NOT_FOUND,
                    data=None,
                    errors=None,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )


class MyCourse(APIView):
    serializer_class = StudentCourseSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
           
            student = Student.objects.filter(user__id = request.user.id).last()
            if student:
                serializer = self.serializer_class(student)
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_200_OK,
                    data=serializer.data,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_404_NOT_FOUND,
                    data=None,
                    errors=None,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )


class MyCourseDetails(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request,course_id = None):
        try:
            if course_id:
                student = Student.objects.get(user__id = request.user.id)
                enrolled_course = student.enrolled_course.get(id=course_id)
                course_details = {
                    'id': enrolled_course.id,
                    'name': enrolled_course.course_name,
                    'description': enrolled_course.description,
                    'specifications': enrolled_course.specifications,
                    'price': enrolled_course.price
                }
            if student:
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_200_OK,
                    data=course_details,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_404_NOT_FOUND,
                    data=None,
                    errors=None,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )


class StudentCertificateApiView(APIView):
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            student_certificate = Certificate.objects.filter(student__user__id = request.user.id).last()
            if student_certificate:
                serializer = self.serializer_class(student_certificate)
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_200_OK,
                    data=serializer.data,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_404_NOT_FOUND,
                    data=None,
                    errors=None,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )


class CreateRetriveAllQuery(generics.ListCreateAPIView):
    serializer_class = QueriesReplySerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            queries = Queries.objects.filter(student__user_id=request.user.id)
            if queries:
                data = []
                for query in queries:
                    queries_serializer = QueriesSerializer(query)
                    reply_threads = ReplyThread.objects.filter(queries=query)
                    results_serializer = ReplyThreadSerializer(reply_threads, many=True)
                    data.append({
                        "queries": queries_serializer.data,
                        "results": results_serializer.data,
                    })
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_200_OK,
                    data=data,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_404_NOT_FOUND,
                    data=None,
                    errors=None,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )

   
    def post(self, request, format=None):
        try:
            data =  request.data
            data['student'] = Student.objects.get(user = request.user).id
            serializer = QueriesSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_201_CREATED,
                    data=serializer.data,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_400_BAD_REQUEST,
                    data=None,
                    errors=serializer.errors,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )
    

class CreateReplyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data =  request.data
            serializer = QueriesReplyCreateSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_201_CREATED,
                    data=serializer.data,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_400_BAD_REQUEST,
                    data=None,
                    errors=serializer.errors,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )
    

class RetriveAllReplyAPIView(APIView):
    serializer_class = QueriesReplySerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, reply_id):
        try:
            student = ReplyThread.objects.filter(queries__student__user__id = request.user.id, queries = reply_id)
            if student:
                serializer = self.serializer_class(student, many = True)
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_200_OK,
                    data=serializer.data,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_404_NOT_FOUND,
                    data=None,
                    errors=None,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )
    

class StudentCourseDetails(APIView):
    serializer_class = StudentCourseDetailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            student = UserCourse.objects.filter(student__user__id = request.user.id)
            if student:
                serializer = self.serializer_class(student, many = True,context = {'request' : request})
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_200_OK,
                    data=serializer.data,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_404_NOT_FOUND,
                    data=None,
                    errors=None,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )

class StudentCourseDetailsAPI(APIView):
    serializer_class = StudentCourseDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request,course_id):
        try:
            student = UserCourse.objects.filter(student__user__id = request.user.id, id = course_id).first()
            if student:
                serializer = self.serializer_class(student, context = {'request' : request})
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_200_OK,
                    data=serializer.data,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_404_NOT_FOUND,
                    data=None,
                    errors=None,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )
        
class StudentCourseModuleAPIView(APIView):
    serializer_class = StudentCourseModuleSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request,course_id):
        try:
            student = UserCourseModule.objects.filter(course_name__student__user__id = request.user.id,course_name__id = course_id).order_by('id')
            if student:
                serializer = self.serializer_class(student, many = True,context = {'request' : request})
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_200_OK,
                    data=serializer.data,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_404_NOT_FOUND,
                    data=None,
                    errors=None,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )

class StudentCourseModuleDetailsAPIView(APIView):
    serializer_class = StudentCourseModuleDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, syallbus_id):
        try:
            student = SubSyllabus.objects.filter(syllabus__id = syallbus_id)
            if student:
                serializer = self.serializer_class(student, many = True)
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_200_OK,
                    data=serializer.data,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_404_NOT_FOUND,
                    data=None,
                    errors=None,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )


class FakeEntryDelete(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data['email']
        fake_entry = EnquirersForms.objects.filter(email= email)
        fake_entry.delete()
        return create_response_util.create_response_data(
                    message="Success",
                    status=status.HTTP_200_OK,
                    data=None,
                    errors={'email': 'Fake Entry Successfully Deleted'},
                )


class RevisionTest(APIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id, syllabus_id):
        try:
            questions = Question.objects.filter(
                course__id=course_id,
                syllabus__id=syllabus_id, 
                test_type='Revision Test',
                )
            if questions:
                serializer = self.serializer_class(questions, many = True)
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_200_OK,
                    data=serializer.data,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="no questions found",
                    status=status.HTTP_404_NOT_FOUND,
                    data=None,
                    errors=None,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )
        

class PracticeTest(APIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id, syllabus_id):
        try:
            questions = Question.objects.filter(
                course__id=course_id,
                syllabus__id=syllabus_id,
                test_type='Practice Test'
                )
            if questions:
                serializer = self.serializer_class(questions, many = True)
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_200_OK,
                    data=serializer.data,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="no questions found",
                    status=status.HTTP_404_NOT_FOUND,
                    data=None,
                    errors=None,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )
        

class CreateReplyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data =  request.data
            serializer = QueriesReplyCreateSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_201_CREATED,
                    data=serializer.data,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_400_BAD_REQUEST,
                    data=None,
                    errors=serializer.errors,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )
        

        