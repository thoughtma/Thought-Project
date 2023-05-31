# Django Import
from django.shortcuts import render

# Project Imports
from apps.trainer.models import Trainer
from apps.trainer.serializers import TrainerSerializer
from apps.accounts.utils import create_trainer_user
from apps.accounts import create_response_util
from apps.accounts.models import User

# Third Party Import
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination


class TrainerCreateApiView(generics.ListAPIView):
    serializer_class = TrainerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    # filter_backends = (SearchFilter, DjangoFilterBackend,)
    # search_fields = ['user__first_name']

    def get_queryset(self, *args, **kwargs):
        queryset = Trainer.objects.all()
        return queryset

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def list(self, request):
        try:
            # trainer = self.filter_queryset(self.get_queryset(request))
            trainer = self.get_queryset(request)
            trainers = self.paginate_queryset(trainer)
            serializer = self.serializer_class(trainers, many=True)
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
            serializer = TrainerSerializer(
                data=data, context={'request': request})
            if serializer.is_valid():
                user = create_trainer_user(request.data, "TRAINER")
                serializer.save(user=user)

                # SendMail.user_send_credential_email(
                #     user, password=request.data["password"])
                # SendMail.user_send_welcome_email(user)
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


class TrainerRetriveApiView(APIView):
    serializer_class = TrainerSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            trainer = Trainer.objects.filter(id=id).last()
            if trainer:
                serializer = self.serializer_class(trainer)

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
                    errors=None,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )

    def put(self, request, id):
        try:
            data = request.data
            trainer = Trainer.objects.get(id=id)
            serializer = self.serializer_class(trainer, data=data)
            if serializer.is_valid():
                serializer.save()
                user = User.objects.get(id=trainer.user.id)
                user.email = data["email"]
                user.name = data["name"]
                # user.first_name = data["first_name"]
                # user.last_name = data["last_name"]
                # user_password = data["password"]
                # user.set_password(user_password)
                user.save()
                # SendMail.user_upadte_credential_email(user,password=request.data["password"])
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

    def delete(self, request, id):
        try:
            trainer = Trainer.objects.get(id=id)
            if trainer:
                trainer.is_active = False
                trainer.save()
                user = User.objects.get(id=trainer.user.id)
                user.is_active = False
                user.save()
                return create_response_util.create_response_data(
                    message="success", status=status.HTTP_200_OK, data=None, errors=None
                )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_400_BAD_REQUEST,
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
