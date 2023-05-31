# Python Imports
import logging
import datetime

# Django Import
from django.shortcuts import render, get_object_or_404
from django.http import Http404

# Project Import
from .models import Courses, WhatYouLearn, AboutCourse, CareerPath, TheseCourseIsForYou, Syllabus, SubSyllabus
from .serializers import CoursesSerializer, WhatYouLearnSerializer, AboutCourseSerializer, CareerPathSerializer, TheseCourseIsForYouSerializer, SyllabusSerializer, SubSyllabusSerializer
from apps.accounts import create_response_util
from apps.student.models import UserCourse
# Third Party Import
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination

logger = logging.getLogger(__name__)
info_logger = logging.getLogger('info_logger')
exception_logger = logging.getLogger('exception_logger')
error_logger = logging.getLogger('error_logger')
warning_logger = logging.getLogger('warning_logger')


class CourseListCreateApiView(generics.ListCreateAPIView):
    """
    API view for listing and creating courses.

    get:
    Return a list of all available courses.

    post:
    Create a new course instance.
    """
    serializer_class = CoursesSerializer
    permission_classes = [AllowAny]
    # pagination_class = PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        """
        Return the queryset of all courses.
        """
        queryset = Courses.objects.all()
        return queryset
    
    def list(self, request):
        """
        Return a list of all available courses.
        """
        try:
            info_logger.info('Fetching the list of available courses')
            course = self.get_queryset(request)
            serializer = self.serializer_class(course, many=True)
            info_logger.info('Courses successfully retrieved')
            return create_response_util.create_response_data(
                message="success",
                status=status.HTTP_200_OK,
                data=serializer.data,
                errors=None,
            )
        except Exception as e:
            exception_logger.exception('An exception occurred while fetching the course list')
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )

  
class CourseRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows retrieval, updating and deletion of a single course instance.

    retrieve:
    Return a course instance.

    update:
    Update and return a course instance.

    partial_update:
    Update and return a course instance.

    delete:
    Remove a course instance.

    """
    serializer_class = CoursesSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self, *args, **kwargs):
        """
        Return all courses queryset
        """
        queryset = Courses.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        """
        Retrieve a course instance.
        """
        try:
            info_logger.info('Retrieving a course detais')
            instance = self.get_object()
            serializer = self.serializer_class(instance)
            info_logger.info('Course details successfully retrieved')
            return create_response_util.create_response_data(
                message="success",
                status=status.HTTP_200_OK,
                data=serializer.data,
                errors=None,
            )
        except Exception as e:
            exception_logger.exception('An exception occurred while retrieving the course instance')
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )


 
class WhatYouLearnRetrieveApiView(APIView):
    """
    API endpoint that allows creation and retrieval of WhatYouLearn instances.

    Methods:
        GET:
            Retrieve a list of WhatYouLearn instances.

        POST:
            Create a new WhatYouLearn instance.

    Permissions:
        - User must be authenticated.
        - User must be an admin.

    Returns:
        Serialized data, error message and HTTP status code in JSON format.
    """

    serializer_class = WhatYouLearnSerializer
    permission_classes = [AllowAny]

    def get_queryset(self, user_course_id, *args, **kwargs):
        user_course = UserCourse.objects.get(id = user_course_id)
        course = Courses.objects.filter(id = user_course.course_name.id).first()
        queryset = WhatYouLearn.objects.filter(course_name__course_name=course.course_name)
        return queryset

    def get(self, request, user_course_id, *args, **kwargs):
        try:
            instance = self.get_queryset(user_course_id).first()
            info_logger.info('Retrieving a why you learn instance')
            if not instance:
                warning_logger.warning('Why you learn instance not found')
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_404_NOT_FOUND,
                    data=None,
                    errors="Object not found",
                )
            serializer = self.serializer_class(instance)
            return create_response_util.create_response_data(
                message="success",
                status=status.HTTP_200_OK,
                data=serializer.data,
                errors=None,
            )
        except Exception as e:
            exception_logger.exception('An exception occurred while retrieving the why you learn for course')
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )


class AboutCourseRetrieveAPIView(APIView):
    """
    API view to list and create AboutCourse objects.
    Only admin users are allowed to access this view.

    Methods:
    --------
    get_queryset(*args, **kwargs):
        Returns the queryset of all AboutCourse objects.

    post(request, *args, **kwargs):
        Creates a new AboutCourse object and returns the serialized data.
        Request data should contain all the required fields for AboutCourse object.

    Attributes:
    -----------
    serializer_class:
        AboutCourseSerializer class to serialize/deserialize the AboutCourse objects.

    permission_classes:
        Permission classes which allow only admin users to access this view.
    """
    serializer_class = AboutCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, user_course_id, *args, **kwargs):
        user_course = UserCourse.objects.get(id = user_course_id)
        course = Courses.objects.filter(id = user_course.course_name.id).first()
        queryset = AboutCourse.objects.filter(course_name__course_name=course.course_name)
        return queryset

    def get(self, request, user_course_id, *args, **kwargs):
        try:
            info_logger.info('Retrieving About course instance')
            instance = self.get_queryset(user_course_id).first()
            if not instance:
                warning_logger.warning('About Course instance not found')
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_404_NOT_FOUND,
                    data=None,
                    errors="Object not found",
                )
            serializer = self.serializer_class(instance)
            return create_response_util.create_response_data(
                message="success",
                status=status.HTTP_200_OK,
                data=serializer.data,
                errors=None,
            )
        except Exception as e:
            exception_logger.exception('An exception occurred while retrieving the About course')
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )



class CareerPathRetrieveApiView(APIView):
    """
    API view that allows to list and create career paths.

    Inherits from `generics.ListCreateAPIView`, which provides default implementations for the
    `GET` (list) and `POST` (create) methods.

    Attributes:
        serializer_class: The serializer class to be used for the view, which specifies the
            fields to be included in the serialized representation of the career path.
        permission_classes: The list of permission classes that the view requires in order to
            be accessed. In this case, only admin users are allowed.
    """
    serializer_class = CareerPathSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, user_course_id, *args, **kwargs):
        user_course = UserCourse.objects.get(id = user_course_id)
        course = Courses.objects.filter(id=user_course.course_name.id).first()
        queryset = CareerPath.objects.filter(course_name__course_name=course.course_name)
        return queryset

    def get(self, request, user_course_id, *args, **kwargs):
        """
        Create a new career path.

        Args:
            request: The `POST` request containing the data for the new career path.

        Returns:
            A response indicating the result of the creation operation, with a success or failure
            message and the serialized data of the new career path if successful.
        """
        try:
            info_logger.info('Retrieving Career Path instance')
            instance = self.get_queryset(user_course_id).first()
            if not instance:
                warning_logger.warning('Career Path instance not found')
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_404_NOT_FOUND,
                    data=None,
                    errors="Object not found",
                )
            serializer = self.serializer_class(instance)
            return create_response_util.create_response_data(
                message="success",
                status=status.HTTP_200_OK,
                data=serializer.data,
                errors=None,
            )
        except Exception as e:
            exception_logger.exception('An exception occurred while retrieving the Career Path ')
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )


class TheseCourseIsForYouRetrieveApiView(APIView):
    """
    API view to retrieve 'TheseCourseIsForYou' objects for a specific course.

    Required Parameters:
    - pk: primary key of the course to retrieve 'TheseCourseIsForYou' objects for.

    Methods:
    - get: retrieve 'TheseCourseIsForYou' object for a specific course.

    Returns:
    - If successful:
        - message: "success"
        - status: HTTP_200_OK
        - data: serialized 'TheseCourseIsForYou' object
        - errors: None
    - If unsuccessful:
        - message: "failed"
        - status: HTTP_404_NOT_FOUND or HTTP_500_INTERNAL_SERVER_ERROR
        - data: None
        - errors: error message
    """
    serializer_class = TheseCourseIsForYouSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, user_course_id, *args, **kwargs):
        user_course = UserCourse.objects.get(id = user_course_id)
        course = Courses.objects.filter(id=user_course.course_name.id).first()
        queryset = TheseCourseIsForYou.objects.filter(course_name__course_name=course.course_name)
        return queryset

    def get(self, request, user_course_id, *args, **kwargs):
        try:
            info_logger.info('Retrieving These Course For You instance')
            instance = self.get_queryset(user_course_id).first()
            if not instance:
                warning_logger.warning('These Course for you instance not found')
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_404_NOT_FOUND,
                    data=None,
                    errors="Object not found",
                )
            serializer = self.serializer_class(instance)
            return create_response_util.create_response_data(
                message="success",
                status=status.HTTP_200_OK,
                data=serializer.data,
                errors=None,
            )
        except Exception as e:
            exception_logger.exception('An exception occurred while retrieving the These Course for you')
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )


class SyllabusRetrieveApiView(APIView):
    """
    A view that handles listing and creating syllabus objects.

    To list all syllabus objects, send a GET request to this view's endpoint.
    To create a new syllabus object, send a POST request to this view's endpoint
    with the required data in the request body.

    Only authenticated users with admin privileges are allowed to access this view.

    Serializer: SyllabusSerializer

    Methods:
    - get_queryset(*args, **kwargs): Returns a QuerySet containing all syllabus objects.
    - post(request, *args, **kwargs): Creates a new syllabus object with the data provided
      in the request body.
    """
    serializer_class = SyllabusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, user_course_id, *args, **kwargs):
        user_course = UserCourse.objects.get(id = user_course_id)
        course = Courses.objects.filter(id=user_course.course_name.id).first()
        queryset = Syllabus.objects.filter(course_name__course_name=course.course_name)
        return queryset

    def get(self, request, user_course_id, *args, **kwargs):
        try:
            info_logger.info('Retrieving Syllabus instance')
            instance = self.get_queryset(user_course_id).first()
            if not instance:
                warning_logger.warning('Syllabus instance not found')
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_404_NOT_FOUND,
                    data=None,
                    errors="Object not found",
                )
            serializer = self.serializer_class(instance)
            return create_response_util.create_response_data(
                message="success",
                status=status.HTTP_200_OK,
                data=serializer.data,
                errors=None,
            )
        except Exception as e:
            exception_logger.exception('An exception occurred while retrieving the Syllabus')
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )


class SubSyllabusRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubSyllabusSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = SubSyllabus.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        try:
            info_logger.info('Retrieving Sub Syllabus instance')
            instance = self.get_object()
            serializer = self.serializer_class(instance)
            return create_response_util.create_response_data(
                message="success",
                status=status.HTTP_200_OK,
                data=serializer.data,
                errors=None,
            )
        except Exception as e:
            exception_logger.exception('An exception occurred while retrieving the Sub Syllabus')
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )


class PopularCoursesAPIView(generics.ListAPIView):
    serializer_class = CoursesSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset = Courses.objects.all()
        return queryset

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def list(self, request):
        try:
            info_logger.info('Retrieving Popular Courses instance')
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
            exception_logger.exception('An exception occurred while retrieving the Popular Courses')
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )

