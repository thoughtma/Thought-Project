# Python Import
import sys
import datetime
import traceback
import pytz

# Django Import
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ValidationError
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.urls import reverse

# Project Import
from apps.student.models import Student, StudentReviews, UserCourse, UserCourseModule
from apps.accounts.models import User
from apps.accounts.utils import send_student_credential, send_trainer_credential
from apps.courses.models import Courses, WhatYouLearn, AboutCourse, CareerPath, Syllabus, SubSyllabus
from apps.customadmin.forms import StudentForm, UserForm, CourseForm, WhatYouLearnForm, AboutCourseForm, CareerPathForm, SyllabusForm, SubSyllabusForm
from apps.trainer.models import Trainer, LectureVideo, Queries
from apps.common.models import Paymentlog
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password

# Third Party Import
from io import BytesIO
from xhtml2pdf import pisa


'''APIs for admin '''


@login_required
def admin_dashboard(request):
    try:
        return render(request, 'custom_admin/admin_base.html', {})
    except Exception as e:
        return render(request, 'custom_admin/error.html', {'message': f'An error occurred: {e}'})


def admin_login(request):
    try:
        if request.user.is_authenticated:
            return redirect('dashboard')

        if request.method == 'POST':
            username = request.POST.get('email')
            password = request.POST.get('password')
            user_obj = authenticate(email=username, password=password)

            # if user_obj is not None and user_obj.is_superuser:
            if user_obj is not None :
                login(request, user_obj)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid login credentials')

        return render(request, 'custom_admin/accounts/admin_login.html')
    except Exception as e:
        return render(request, 'custom_admin/error.html', {'message': f'An error occurred: {e}'})


@login_required
def admin_logout(request):
    try:
        logout(request)
        return redirect('admin_login')
    except Exception as e:
        return render(request, 'custom_admin/error.html', {'message': f'An error occurred: {e}'})


@login_required
def profile(request):
    user = request.user
    data = User.objects.filter(email=user)

    context = {'user': user, 'data': data}
    return render(request, 'custom_admin/accounts/user_profile.html', context)


def change_password(request):
    try:
        if request.method == 'POST':
            new_password = request.POST['newpassword']
            confirm_password = request.POST['renewpassword']
            user = User.objects.get(email=request.user)
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(
                    request, "Password has been changed successfully.")
                return redirect('admin_login')
            else:
                messages.info(
                    request, "New password and confirm password does not match.")
                return redirect('change_password')
        return render(request, "custom_admin/accounts/change_password.html")
    except Exception as e:
        return render(request, 'custom_admin/error.html', {'message': f'An error occurred: {e}'})


@login_required
def admin_dashboard(request):
    try:
        context = {}
        students = Student.objects.all().count()
        users = User.objects.all().count()
        courses = Courses.objects.all().count()
        enquiry_forms = EnquirersForms.objects.all().count()
        contact_forms = ContactForms.objects.all().count()
        reviews = StudentReviews.objects.all().count()
        trainers = Trainer.objects.all().count()
        payments = Paymentlog.objects.aggregate(
            Sum('price'))['price__sum'] or 0
        unanswered_queries = Queries.objects.filter(
            student__isnull=False, query__isnull=False).exclude(query__exact='').count()

        context['students'] = students
        context['users'] = users
        context['courses'] = courses
        context['enquiry_forms'] = enquiry_forms
        context['contact_forms'] = contact_forms
        context['reviews'] = reviews
        context['trainers'] = trainers
        context['payments'] = payments
        context['unanswered_queries'] = unanswered_queries
        return render(request, 'custom_admin/admin_dashboard.html', context)
    except Exception as e:
        return render(request, 'custom_admin/error.html', {'message': f'An error occurred: {e}'})


@login_required
def admin_test(request):
    try:
        context = {}
        return render(request, 'custom_admin/accounts/register.html', context)
    except Exception as e:
        return render(request, 'custom_admin/error.html', {'message': f'An error occurred: {e}'})


'''APIs for users'''

@login_required
def all_users(request):
    try:
        form = UserForm()
        users = User.objects.filter(user_type = "SUPERADMIN").order_by('-id')
        if request.method == 'POST':
            selected_groups = request.POST.getlist('groups')
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = True
                # user.save()
                user.user_type = "SUPERADMIN"
                user.set_password(password)
                users = user.save()
                # form.save_m2m()
                # permissions = form.cleaned_data['permissions']
                # user.user_permissions.set(permissions)

                # group = Group.objects.get(name='Students')
                # users.group.add(group)
                for group_name in selected_groups:
                    group = Group.objects.get(name=group_name)
                    user.groups.add(group)
                return redirect('users')
        return render(request, 'custom_admin/accounts/all_users.html', {'form': form, "users": users})
    except Exception as e:
        return render(request, 'custom_admin/error.html', {'message': f'An error occurred: {e}'})

def user_delete(request,id):
    users = User.objects.filter(id = id, user_type = "SUPERADMIN")
    users.delete()
    return redirect('users')

@login_required
def user_detail_view(request,id):
    try:
        user = User.objects.get(id = id)
        permissions = user.groups.all()
        return render(request, 'custom_admin/accounts/user_detailview.html', {'user' : user, 'permissions': permissions})
    except Exception as e:
        return render(request, 'custom_admin/error.html', {'message': f'An error occurred: {e}'})


# @login_required
# def user_update(request, id):
#     try:
#         user = get_object_or_404(User, id=id)
#         # breakpoint()
#         if request.method == 'POST':

#             form = UserUpdateForm(request.POST, instance=user)
#             print(form)
#             if form.is_valid():
#                 form.save()
#                 return redirect('users')
#         else:
#             form = UserUpdateForm(instance=user)
#         return render(request, 'custom_admin/accounts/user_update.html', {'form': form})
#     except (Courses.DoesNotExist, ValidationError):
#         return render(request, 'custom_admin/error.html', {'message': 'Invalid user ID or form data.'})



@login_required
def user_update(request, id):
    try:
        user = get_object_or_404(User, id=id)
        all_groups = Group.objects.all()  # Fetch all groups
        selected_groups = user.groups.all()
        if request.method == 'POST':
            form = UserUpdateForm(request.POST, instance=user)
            if form.is_valid():
                user = form.save(commit=False)
                selected_groups = request.POST.getlist('groups')
                user.groups.clear()  # Clear existing group memberships
                for group_name in selected_groups:
                    group = Group.objects.get(name=group_name)
                    user.groups.add(group)
                user.save()
                return redirect('users')
        else:
            form = UserUpdateForm(instance=user)
        return render(request, 'custom_admin/accounts/user_update.html', {'form': form, 'all_groups': all_groups, 'selected_groups': selected_groups})
    except (User.DoesNotExist, ValidationError):
        return render(request, 'custom_admin/error.html', {'message': 'Invalid user ID or form data.'})



@login_required
def change_user_status(request, id):
    uact = get_object_or_404(User, id=id)
    if uact.is_active and uact.is_superuser == False:
        uact.is_active = False
        uact.save()
        return redirect('users')
    else:
        uact.is_active = True
        uact.save()
        return redirect('users')


''' APIs for Courses Module'''


@login_required
def courses(request):
    courses = Courses.objects.all()
    return render(request, 'custom_admin/courses/courses.html', {'courses':courses})


@login_required
def add_course(request):
    try:
        form = CourseForm()
        if request.method == 'POST':
            form = CourseForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Course has been created.')
                return redirect('course_list')
            else:
                messages.error(request, 'There was an error creating the course. Please check the form and try again.')
        context = {'form': form}
        return render(request, 'custom_admin/courses/add_course.html', context)
    except Exception as e:
        messages.error(request, f"There was an error: {str(e)}")
        return redirect('courses')



@login_required
def course_detail(request, id):
    try:
        course = get_object_or_404(Courses, id=id)
    except Courses.DoesNotExist:
        raise Http404("Course does not exist")
    except Exception as e:
        return render(request, 'custom_admin/error.html', {'error_message': str(e)})
    else:
        return render(request, 'custom_admin/courses/course_detail.html', {'course': course})


@login_required
def course_update(request, id):
    try:
        course = get_object_or_404(Courses, id=id)
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES, instance=course)
            if form.is_valid():
                form.save()
                return redirect('courses')
        else:
            form = CourseForm(instance=course)
        return render(request, 'custom_admin/courses/course_update.html', {'form': form})
    except (Courses.DoesNotExist, ValidationError):
        return render(request, 'custom_admin/error.html', {'message': 'Invalid course ID or form data.'})


@login_required
def course_delete(request, id):
    course = get_object_or_404(Courses, id=id)
    course.delete()
    return redirect('courses')


@login_required
def course_changestatus(request, id):
    course = get_object_or_404(Courses, id=id)
    if course.is_active:
        course.is_active = False
        course.save()
        return redirect('courses')
    else:
        course.is_active = True
        course.save()
        return redirect('courses')


@login_required
def course_changestatus(request, id):
    course = get_object_or_404(Courses, id=id)
    if course.is_active:
        course.is_active = False
        course.save()
        return redirect('courses')
    else:
        course.is_active = True
        course.save()
        return redirect('courses')



''' APIs for What You Learn '''

@login_required
def whatyoulearn(request):
    try:
        form = WhatYouLearnForm()
        courses = WhatYouLearn.objects.all()
        if request.method == 'POST':
            form = WhatYouLearnForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('whatyoulearn')
        return render(request, 'custom_admin/courses/whatyoulearn.html', {"form": form, "courses": courses})
    except Exception as e:
        return render(request, 'custom_admin/error.html', {'message': f'An error occurred: {e}'})


@login_required
def whatyoulearn_detail(request, id):
    try:
        course = get_object_or_404(WhatYouLearn, id=id)
        return render(request, 'custom_admin/courses/whatyoulearn_detail.html', {'course': course})
    except Exception as e:
        return render(request, 'custom_admin/error.html', {'message': f'An error occurred: {e}'})


@login_required
def whatyoulearn_update(request, id):
    course = get_object_or_404(WhatYouLearn, id=id)
    if request.method == 'POST':
        form = WhatYouLearnForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('whatyoulearn')
    else:
        form = WhatYouLearnForm(instance=course)
    return render(request, 'custom_admin/courses/whatyoulearn_update.html', {'form': form})


@login_required
def whatyoulearn_delete(request, id):
    course = get_object_or_404(WhatYouLearn, id=id)
    course.delete()
    return redirect('whatyoulearn')


''' APIs for AboutCourse '''

@login_required
def aboutcourse(request):
    form = AboutCourseForm()
    courses = AboutCourse.objects.all()
    if request.method == 'POST':
        form = AboutCourseForm(request.POST, request.FILES)
        if form.is_valid():
            about_course = form.save(commit=False)
            image_file = request.FILES.get('about_course_image')
            if image_file:
                filename = default_storage.save(
                    image_file.name, ContentFile(image_file.read()))
                about_course.about_course_image = filename
            about_course.save()
            return redirect('aboutcourse')

    return render(request, 'custom_admin/courses/aboutcourse.html', {"form": form, "courses": courses})


@login_required
def aboutcourse_detail(request, id):
    course = get_object_or_404(AboutCourse, id=id)
    return render(request, 'custom_admin/courses/aboutcourse_detail.html', {'course': course})


@login_required
def aboutcourse_update(request, id):
    course = get_object_or_404(AboutCourse, id=id)
    if request.method == 'POST':
        form = AboutCourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            about_course = form.save(commit=False)
            image_file = request.FILES.get('about_course_image')
            if image_file:
                filename = default_storage.save(
                    image_file.name, ContentFile(image_file.read()))
                about_course.about_course_image = filename
            about_course.save()
            return redirect('aboutcourse')
    else:
        form = AboutCourseForm(instance=course)
    return render(request, 'custom_admin/courses/aboutcourse_update.html', {'form': form})


@login_required
def aboutcourse_delete(request, id):
    course = get_object_or_404(AboutCourse, id=id)
    course.delete()
    return redirect('aboutcourse')


''' APIs for CareerPath '''

@login_required
def career_path(request):
    form = CareerPathForm()
    courses = CareerPath.objects.all()
    if request.method == 'POST':
        form = CareerPathForm(request.POST, request.FILES)
        if form.is_valid():
            career_path = form.save(commit=False)
            image_file = request.FILES.get('career_path_image')
            if image_file:
                filename = default_storage.save(
                    image_file.name, ContentFile(image_file.read()))
                career_path.career_path_image = filename
            career_path.save()
            return redirect('career_path')
    return render(request, 'custom_admin/courses/career_path.html', {"form": form, "courses": courses})


@login_required
def career_path_detail(request, id):
    course = get_object_or_404(CareerPath, id=id)
    return render(request, 'custom_admin/courses/career_path_detail.html', {'course': course})


@login_required
def career_path_update(request, id):
    course = get_object_or_404(CareerPath, id=id)
    if request.method == 'POST':
        form = CareerPathForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            career_path = form.save(commit=False)
            image_file = request.FILES.get('career_path_image')
            if image_file:
                filename = default_storage.save(
                    image_file.name, ContentFile(image_file.read()))
                career_path.career_path_image = filename
            career_path.save()
            return redirect('career_path')
    else:
        form = CareerPathForm(instance=course)
    return render(request, 'custom_admin/courses/career_path_update.html', {'form': form})


@login_required
def career_path_delete(request, id):
    course = get_object_or_404(CareerPath, id=id)
    course.delete()
    return redirect('career_path')


''' APIs for Syllabus '''

@login_required
def syllabus(request):
    form = SyllabusForm()
    courses = Syllabus.objects.all()
    if request.method == 'POST':
        form = SyllabusForm(request.POST, request.FILES)
        if form.is_valid():
            syllabus = form.save(commit=False)
            image_file = request.FILES.get('syllabus_image')
            if image_file:
                filename = default_storage.save(
                    image_file.name, ContentFile(image_file.read()))
                syllabus.syllabus_image = filename
            syllabus.save()
            return redirect('syllabus')
    return render(request, 'custom_admin/courses/syllabus.html', {"form": form, "courses": courses})


@login_required
def syllabus_detail(request, id):
    course = get_object_or_404(Syllabus, id=id)
    return render(request, 'custom_admin/courses/syllabus_detail.html', {'course': course})


@login_required
def syllabus_update(request, id):
    course = get_object_or_404(Syllabus, id=id)
    if request.method == 'POST':
        form = SyllabusForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            syllabus = form.save(commit=False)
            image_file = request.FILES.get('syllabus_image')
            if image_file:
                filename = default_storage.save(
                    image_file.name, ContentFile(image_file.read()))
                syllabus.syllabus_image = filename
            syllabus.save()
            return redirect('syllabus')
    else:
        form = SyllabusForm(instance=course)
    return render(request, 'custom_admin/courses/syllabus_update.html', {'form': form})


@login_required
def syllabus_delete(request, id):
    course = get_object_or_404(Syllabus, id=id)
    course.delete()
    return redirect('syllabus')


@login_required
def syllabus_changestatus(request, id):
    syllabus = get_object_or_404(Syllabus, id=id)
    if syllabus.is_active:
        syllabus.is_active = False
        syllabus.save()
        return redirect('syllabus')
    else:
        syllabus.is_active = True
        syllabus.save()
        return redirect('syllabus')


@login_required
def syllabus_changestatus(request, id):
    syllabus = get_object_or_404(Syllabus, id=id)
    if syllabus.is_active:
        syllabus.is_active = False
        syllabus.save()
        return redirect('syllabus')
    else:
        syllabus.is_active = True
        syllabus.save()
        return redirect('syllabus')



''' APIs for SubSyllabus '''

@login_required
def subsyllabus(request):
    form = SubSyllabusForm()
    courses = SubSyllabus.objects.all()
    if request.method == 'POST':
        form = SubSyllabusForm(request.POST, request.FILES)
        if form.is_valid():
            subsyllabus = form.save(commit=False)
            image_file = request.FILES.get('sub_syllabus_image')
            if image_file:
                filename = default_storage.save(
                    image_file.name, ContentFile(image_file.read()))
                subsyllabus.sub_syllabus_image = filename
            subsyllabus.save()
            return redirect('subsyllabus')
    return render(request, 'custom_admin/courses/subsyllabus.html', {"form": form, "courses": courses})


@login_required
def subsyllabus_detail(request, id):
    course = get_object_or_404(SubSyllabus, id=id)
    return render(request, 'custom_admin/courses/subsyllabus_detail.html', {'course': course})


@login_required
def subsyllabus_update(request, id):
    course = get_object_or_404(SubSyllabus, id=id)
    if request.method == 'POST':
        form = SubSyllabusForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            subsyllabus = form.save(commit=False)
            image_file = request.FILES.get('sub_syllabus_image')
            if image_file:
                filename = default_storage.save(
                    image_file.name, ContentFile(image_file.read()))
                subsyllabus.sub_syllabus_image = filename
            subsyllabus.save()
            return redirect('subsyllabus')
    else:
        form = SubSyllabusForm(instance=course)
    return render(request, 'custom_admin/courses/syllabus_update.html', {'form': form})


@login_required
def subsyllabus_delete(request, id):
    course = get_object_or_404(SubSyllabus, id=id)
    course.delete()
    return redirect('subsyllabus')


@login_required
def subsyllabus_changestatus(request, id):
    subsyllabus = get_object_or_404(SubSyllabus, id=id)
    if subsyllabus.is_active:
        subsyllabus.is_active = False
        subsyllabus.save()
        return redirect('subsyllabus')
    else:
        subsyllabus.is_active = True
        subsyllabus.save()
        return redirect('subsyllabus')


@login_required
def subsyllabus_changestatus(request, id):
    subsyllabus = get_object_or_404(SubSyllabus, id=id)
    if subsyllabus.is_active:
        subsyllabus.is_active = False
        subsyllabus.save()
        return redirect('subsyllabus')
    else:
        subsyllabus.is_active = True
        subsyllabus.save()
        return redirect('subsyllabus')


'''APIs For Student '''

@login_required
def student(request):
    form = StudentForm()
    students = Student.objects.all().order_by('-id')

    if request.method == 'POST':
        form = StudentForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if form.is_valid():
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')

            else:
                user = User.objects.create(
                    email=form.cleaned_data['email'],
                    name=form.cleaned_data['name'],
                    contact=form.cleaned_data['contact'],
                    password=make_password(form.cleaned_data['password']),
                    is_active=True
                )
                student = form.save(commit=False)
                student.user = user
                student.save()
                enrolled_courses = form.cleaned_data['enrolled_course']
                student.enrolled_course.set(enrolled_courses)
                send_student_credential(email, name, password)
                for course_name in enrolled_courses:
                    try:
                        course = Courses.objects.get(course_name = course_name)
                    except Exception as e:
                        print(e)
                    student_course = UserCourse.objects.create(course_name = course, student = student)
                    student_course.save()
                    first_module_unlocked = True
                    syllabus = Syllabus.objects.filter(course_name=course)
                    for module in syllabus:
                        if first_module_unlocked:
                            syllabus_status = "START MODULE"
                            first_module_unlocked = False
                        else:
                            syllabus_status = "LOCKED"

                        user_module = UserCourseModule.objects.create(course_name=student_course, syllabus=module, syllabus_status=syllabus_status)
                        user_module.save()
                return redirect('add-student')
        else:
            messages.error(
                request, 'Form is not valid. Please check your input.')

    return render(request, 'custom_admin/student/add_student.html', {'form': form, 'students': students})


@login_required
def student_detail_view(request, id):
    student = get_object_or_404(Student, pk=id)
    context = {'student': student}
    return render(request, 'custom_admin/student/student_detailview.html', context)


@login_required
def changestatus(request, myid):
    uact = get_object_or_404(User, pk=myid)
    if uact.is_active:
        uact.is_active = False
        uact.save()
        return redirect('add-student')
    else:
        uact.is_active = True
        uact.save()
        return redirect('add-student')


@login_required
def student_update(request, id):
    student = get_object_or_404(Student, pk=id)
    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, instance=student)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exclude(id=student.user.id).exists():
                form.errors['email'] = 'This email is already in use.'
                return render(request, 'custom_admin/update_student.html', {'form': form})
            student = form.save(commit=False)
            student.user.email = email
            student.user.save()
            student.save()
            form.save_m2m()
            enrolled_courses = form.cleaned_data['enrolled_course']
            UserCourse.objects.filter(student = student).delete()
            for course_name in enrolled_courses:
                course = Courses.objects.get(course_name = course_name)
                if not UserCourse.objects.filter(course_name = course, student = student).exists():
                    student_course = UserCourse.objects.create(course_name = course, student = student)
                    student_course.save()
                    first_module_unlocked = True
                    syllabus = Syllabus.objects.filter(course_name=course)
                    for module in syllabus:
                        if first_module_unlocked:
                            syllabus_status = "START MODULE"
                            first_module_unlocked = False
                        else:
                            syllabus_status = "LOCKED"

                        user_module = UserCourseModule.objects.create(course_name=student_course, syllabus=module, syllabus_status=syllabus_status)
                        user_module.save()
            return redirect('add-student')
    else:
        form = StudentUpdateForm(
            instance=student,
            initial={
                'name': student.user.name,
                'email': student.user.email,
                'contact': student.user.contact,
                'highest_qualification': student.highest_qualification,
                'category': student.category,
                'local_address': student.local_address,
                # 'permanent_address': student.permanent_address,
                'father_name': student.father_name,
                'father_mobile_number': student.father_mobile_number,
                'enrolled_course': student.enrolled_course.all(),
            }
        )
    return render(request, 'custom_admin/student/update_student.html', {'form': form})


@login_required
def student_delete(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    return redirect('add-student')


'''APIs for Trainer'''


from django.http import JsonResponse
from django.contrib import messages
@login_required
# @login_required
def check_email(request, email):
    print('rererer',email)
    breakpoint()
    if request.method == 'GET':
        email = request.GET.get('email')

        if Trainer.objects.filter(email=email).exists():
            return JsonResponse({'exists': True})
        else:
            return JsonResponse({'exists': False})

@login_required
def all_trainer(request):
    form = TrainerForm()

    if request.method == 'POST':
        form = TrainerForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            if Trainer.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
            else:
                form.save()
                # send_trainer_credential(email, name)
                return redirect('trainer')
    else:
        form = TrainerForm()
    trainer = Trainer.objects.all().order_by('-id')
    return render(request, 'custom_admin/trainer/all_trainer.html', {'form': form, 'trainer': trainer})


@login_required
def trainer_changestatus(request, id):
    uact = get_object_or_404(Trainer, pk=id)
    if uact.is_active:
        uact.is_active = False
        uact.save()
        return redirect('trainer')
    else:
        uact.is_active = True
        uact.save()
        return redirect('trainer')


@login_required
def trainer_detail_view(request, id):
    trainer = get_object_or_404(Trainer, id=id)
    return render(request, 'custom_admin/trainer/trainer_detail_view.html', {'trainer': trainer})


@login_required
def trainer_update(request, id):
    trainer = get_object_or_404(Trainer, pk=id)
    if request.method == 'POST':
        form = UpdateTrainerForm(request.POST, instance=trainer)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if Trainer.objects.filter(email=email).exclude(id=trainer.id).exists():
                form.errors['email'] = 'This email is already in use.'
                return render(request, 'custom_admin/update_trainer.html', {'form': form, 'trainer': trainer})
            trainer = form.save(commit=False)
            trainer.email = email
            trainer.save()
            return redirect('trainer-detail-view', id=id) 
    else:
        form = UpdateTrainerForm(instance=trainer, initial={
            'name': trainer.name,
            'email': trainer.email,
            'contact': trainer.contact,
            'specialization': trainer.specialization,
            'experience': trainer.experience,
            'address': trainer.address

        })
    return render(request, 'custom_admin/trainer/update_trainer.html', {'form': form, 'trainer': trainer})


@login_required
def trainer_delete(request, id):
    trainer = Trainer.objects.get(id=id)
    trainer.delete()
    return redirect("trainer")


@login_required
def trainer_lecturevideo(request):
    lecturevideo = None
    if request.method == 'POST':
        form = LectureVideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'lecturevideo added successfully.!')
            return redirect('trainer-lecturevideo')
        # messages.error(request, 'Trainer already Exists..')
    else:
        form = LectureVideoForm()
        lecturevideos = LectureVideo.objects.all()
    return render(request, 'custom_admin/trainer/trainer_lecturevideo.html',
                  {'lecturevideos': lecturevideos, 'form': form
                   })


@login_required
def trainer_play_lecture_video(request, pk):
    lecture_video = get_object_or_404(LectureVideo, pk=pk)
    return render(request, 'custom_admin/trainer/lecturevideo_play.html', {'lecture_video': lecture_video})


@login_required
def trainer_lecturevideo_detail_view(request, id):
    lecturevideo = get_object_or_404(LectureVideo, id=id)
    return render(request, 'custom_admin/trainer/trainer_lecturevideo_detail_view.html', {'lecturevideo': lecturevideo})


@login_required
def trainer_lecturevideo_delete(request, id):
    lecturevideo = LectureVideo.objects.get(id=id)
    lecturevideo.delete()
    return redirect("trainer-lecturevideo")


@login_required
def trainer_lecturevideo_update(request, id):
    lecture_video = get_object_or_404(LectureVideo, pk=id)
    if request.method == 'POST':
        form = LectureVideoForm(
            request.POST, request.FILES, instance=lecture_video)
        if form.is_valid():
            form.save()
            return redirect('trainer-lecturevideo')
    else:
        form = LectureVideoForm(instance=lecture_video)
    return render(request, 'custom_admin/trainer/trainer_update_lecturevideo.html', {'form': form})


# Quries view from here.

# add and show Quires
def show_queries(request):
    try:
        queries = Queries.objects.all().order_by('-id')
        query_list = []
        for query in queries:
            latest_student_thread = ReplyThread.objects.filter(queries=query).order_by('-id').first()
            if latest_student_thread:
                query_list.append(latest_student_thread)

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        queries = None

    return render(request, 'custom_admin/trainer/all_query.html', {'queries': query_list})




@login_required
def query_detail(request, query_id):
    query = get_object_or_404(Queries, id=query_id)
    reply_threads = query.replythread_set.order_by('id')
    last = ReplyThread.objects.filter(queries = query_id).last()
    if request.method == 'POST':
        latest_id = request.POST['reply_id']
        thread = ReplyThread.objects.get(id = latest_id)
        thread.response = request.POST['response']
        thread.response_by = request.user
        thread.save()
        return redirect('query_detail', query_id=query_id)
    else:
        form = QueryThreadForm(initial={'query_id': query_id})  # Pass the query ID as an initial value

    return render(request, 'custom_admin/trainer/query_detail.html',
                  {'query': query, 'reply_threads': reply_threads, 'form': form,'last_reply':last})






@login_required
def query_detail_view(request, id):
    queries = get_object_or_404(Queries, id=id)
    return render(request, 'custom_admin/query_detail_view.html', {'query': queries})


@login_required
def query_delete(request, id):
    query = Queries.objects.get(id=id)
    query.delete()
    return redirect("trainer-quires")




'''APIs for Contact Forms'''


@login_required
def contact_forms(request):
    try:
        form = ContactUsForm()
        contactforms = ContactForms.objects.all()
        context = {'form': form, 'contactforms': contactforms}
        return render(request, 'custom_admin/common/contactus.html', context)

    except Exception as e:
        messages.error(request, f"There was an error: {str(e)}")
        return redirect('contactforms')


@login_required
def contact_form_detail(request, id):
    try:
        contact = get_object_or_404(ContactForms, id=id)
    except ContactForms.DoesNotExist:
        raise Http404("ContactForm does not exist")
    except Exception as e:
        return render(request, 'custom_admin/error.html', {'error_message': str(e)})
    else:
        return render(request, 'custom_admin/common/contactus_detail.html', {'contact': contact})


@login_required
def contact_form_delete(request, id):
    try:
        contact = get_object_or_404(ContactForms, id=id)
        if request.method == 'POST':
            contact.delete()
            return redirect('contactforms')
        return render(request, 'custom_admin/common/contactus_confirm_delete.html', {'contact': contact})
    except Exception as e:
        return render(request, 'custom_admin/error.html', {'message': f'An error occurred: {e}'})


'''APIs for Enquiry Forms'''


@login_required
def enquiry_forms(request):
    try:
        form = EnquiryForm()
        enquiryforms = EnquirersForms.objects.all().order_by('-id')
        context = {'form': form, 'enquiryforms': enquiryforms}
        return render(request, 'custom_admin/common/enquiryform.html', context)

    except Exception as e:
        messages.error(request, f"There was an error: {str(e)}")
        return redirect('enquiryforms')


@login_required
def enquiry_form_detail(request, id):
    try:
        enquiry = get_object_or_404(EnquirersForms, id=id)
    except EnquirersForms.DoesNotExist:
        raise Http404("Enquiry Form does not exist")
    except Exception as e:
        return render(request, 'custom_admin/error.html', {'error_message': str(e)})
    else:
        return render(request, 'custom_admin/common/enquiryform_detail.html', {'enquiry': enquiry})


@login_required
def enquiry_form_update(request, id):
    enquiries = get_object_or_404(EnquirersForms, id=id)
    if request.method == 'POST':
        enquiries.comment = request.POST.get('comment', enquiries.comment)
        enquiries.priority = request.POST.get('priority', enquiries.priority)
        enquiries.save()
        if enquiries.priority == 'Paid':
            # return redirect('invoice')
            invoice_url = reverse('invoice') + f'?id={enquiries.id}'
            return redirect(invoice_url)
        return redirect('enquiryforms')
    return render(request, 'custom_admin/common/enquiryform_update.html', {'enquiries': enquiries})


@login_required
def enquiry_form_delete(request, id):
    enquiry = EnquirersForms.objects.get(id=id)
    enquiry.delete()
    return redirect('enquiryforms')


'''APIs for StudentReviews'''


@login_required
def review_forms(request):
    try:
        form = StudentReviewForm()
        reviewforms = StudentReviews.objects.all()
        context = {'form': form, 'reviewforms': reviewforms}
        return render(request, 'custom_admin/student/reviewform.html', context)

    except Exception as e:
        messages.error(request, f"There was an error: {str(e)}")
        return redirect('reviewforms')


@login_required
def review_form_detail(request, id):
    try:
        review = get_object_or_404(StudentReviews, id=id)
    except StudentReviews.DoesNotExist:
        raise Http404("Review Form does not exist")
    except Exception as e:
        return render(request, 'custom_admin/error.html', {'error_message': str(e)})
    else:
        return render(request, 'custom_admin/student/reviewform_detail.html', {'review': review})


@login_required
def review_form_delete(request, id):
    review = get_object_or_404(StudentReviews, id=id)
    review.delete()
    return redirect('reviewforms')


@login_required
def generate_invoice(request):
    try:
        id = request.GET.get('id')
        enquirer = EnquirersForms.objects.filter(id=id).values_list('name', flat=True)
        name = enquirer[0] if enquirer else None

        template_name = 'custom_admin/common/invoice_form.html'
        context = {"enquirer_name": name}

        indian_timezone = pytz.timezone('Asia/Kolkata')
        current_date = datetime.datetime.now(indian_timezone).strftime('%d/%m/%Y')
        prefix = "TW/T"
        timestamp = datetime.datetime.now(indian_timezone).strftime("%Y%m%d%H%M%S")
        reciept_number = f"{prefix}{timestamp}"

        if request.method == 'POST':
            email = request.user
            user = User.objects.filter(email=email).first()
            if not user:
                raise Exception("User not found.")
            authority_name = user.name
            designation = user.designation
            name = request.POST.get("name")
            amount_received = request.POST.get('amount_received')
            amount_type = request.POST.get('amount_type')
            technology = request.POST.get('technology')
            invoice_data = {
                'reciept_number': reciept_number,
                'current_date': current_date,
                'name': name,
                'amount_received': amount_received,
                'amount_type': amount_type,
                'technology': technology,
                'authority_name': authority_name,
                'designation': designation,
            }
            rendered_template = render_to_string('invoice_template.html', {'invoice_data': invoice_data})
            buffer = BytesIO()
            pisa.CreatePDF(rendered_template, dest=buffer)
            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            # response = HttpResponse(buffer, content_type='mimetype/submimetype')
            response['Content-Disposition'] = 'attachment; filename="Invoice Receipt.pdf"'
            return response

        return render(request, template_name, context)

    except Exception as e:
        error_message = str(e)
        context = {'error_message': error_message}
        return render(request, 'custom_admin/error.html', context)

'''APIs for Revision Test Questions'''

@login_required
def create_question(request):
    try:
        questions = Question.objects.all()
        form = QuestionForm
        if request.method == 'POST':
            form = QuestionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('questions-create')
        else:
            form = QuestionForm()
        return render(request, 'custom_admin/tests/question_list.html', {'form': form ,'questions': questions,})
    except Exception as e:
        return render(request, 'custom_admin/error.html', {'error_message': str(e)})



@login_required
def question_detail(request, id):
    try:
        question = get_object_or_404(Question, id=id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    except Exception as e:
        return render(request, 'custom_admin/error.html', {'error_message': str(e)})
    else:
        return render(request, 'custom_admin/tests/question_detail.html', {'question': question})


@login_required
def question_update(request, id):
    try:
        question = get_object_or_404(Question, id=id)
        if request.method == 'POST':
            form = QuestionForm(request.POST, instance=question)
            if form.is_valid():
                form.save()
                return redirect('questions-create')
        else:
            form = QuestionForm(instance=question)
        return render(request, 'custom_admin/tests/question_update.html', {'form': form})
    except (Question.DoesNotExist, ValidationError):
        return render(request, 'custom_admin/error.html', {'message': 'Invalid question ID or form data.'})


@login_required
def question_delete(request, id):
    question = get_object_or_404(Question, id=id)
    question.delete()
    return redirect("questions-create")


