# Python Import
import sys

# Django Import
from django.shortcuts import render

# Project Import
from .models import OurOffices
from .serializers import OurOfficesSerializer , NewsletterSubscriberSerializer
from apps.accounts import create_response_util
from .utiles import send_mail

# Third Party Import
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, generics
from rest_framework.filters import SearchFilter
from rest_framework import authentication, permissions


class RunCode(APIView):
    def post(self, request, format=None):
        codeareadata = request.data.get('codearea')

        try:
            # save original standart output reference

            original_stdout = sys.stdout
            # change the standard output to the file we created
            sys.stdout = open('file.txt', 'w')

            # execute code

            exec(codeareadata)  # example =>   print("hello world")

            sys.stdout.close()

            sys.stdout = original_stdout  # reset the standard output to its original value

            # finally read output from file and save in output variable

            output = open('file.txt', 'r').read()
            # output

        except Exception as e:
            # to return error in the code
            sys.stdout = original_stdout
            output = str(e)

        # finally return and render index page and send codedata and output to show on page
        return Response({"output": output})


class OurOfficesApiView(generics.ListAPIView):
    serializer_class = OurOfficesSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset = OurOffices.objects.all()
        return queryset

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def list(self, request):
        try:
            # student = self.filter_queryset(self.get_queryset(request))
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


class SubscribeAPIView(APIView):
    serializer_class = NewsletterSubscriberSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = NewsletterSubscriberSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                send_mail(serializer.data['email'], serializer.data['name'])
                return create_response_util.create_response_data(
                        message="Thank you for subscribing to our newsletter!",
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
'''Code for Python Compiler'''
# def index(request):
#     return render(request, 'python_compiler.html')

# def runcode(request):
#     if request.method == "POST":
#         codeareadata = request.POST['codearea']
#         try:
#             original_stdout = sys.stdout
#             sys.stdout = open('file.txt', 'w') #change the standard output to the file we created
#             exec(codeareadata)  #example =>   print("hello world")
#             sys.stdout.close()
#             sys.stdout = original_stdout  #reset the standard output to its original value
#             # finally read output from file and save in output variable
#             output = open('file.txt', 'r').read()

#         except Exception as e:
#             # to return error in the code
#             sys.stdout = original_stdout
#             output = e
#     return render(request , 'python_compiler.html', {"code":codeareadata , "output":output})
import sys
import os
from django.shortcuts import render

def index(request):
    return render(request, 'python_compiler.html')

def runcode(request):
    if request.method == "POST":
        codeareadata = request.POST.get('codearea', '') # set default value to empty string
        try:
            original_stdout = sys.stdout
            sys.stdout = open('file.txt', 'w') # change the standard output to the file we created
            exec(codeareadata)  # example =>   print("hello world")
            sys.stdout.close()
            sys.stdout = original_stdout  # reset the standard output to its original value
            # finally read output from file and save in output variable
            output = open('file.txt', 'r').read()
        except SyntaxError as e:
            output = "Syntax error: " + str(e)
        except Exception as e:
            output = "Error: " + str(e)
        finally:
            # reset stdout in case of exceptions
            sys.stdout = original_stdout
            # delete file
            try:
                os.remove('file.txt')
            except:
                pass
    else:
        # return empty output for GET requests
        codeareadata = ''
        output = ''
    return render(request, 'python_compiler.html', {"code": codeareadata, "output": output})
