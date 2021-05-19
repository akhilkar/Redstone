from django.shortcuts import render, redirect
from django.http import  HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from .models import Courses, CustomUser, Staffs, Subjects, Students
import datetime
#from .forms import Add_Student_form, Add_Staff_form

def Manage_Staff(request):
    if request.user != None:
        if request.user.user_type == '1':
            staffs=Staffs.objects.all()
            context={'staffs':staffs, 'name':request.user.username,}
            return render(request, 'manage_staff.html', context)

def Add_Staff(request):
    if request.user != None:
        if request.user.user_type == '1':
            return render(request, 'add_staff.html', {'name':request.user.username})

def add_staff_Save(request):
    if request.user != None:
        if request.user.user_type == '1':
            if request.method != 'POST':
                return HttpResponse("Method Not Allowed")
            else:
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                username = request.POST.get('username')
                password = request.POST.get('password')
                address = request.POST.get('address')
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name,profile_pic)
                profile_pic_url = fs.url(filename)
                user = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password, user_type = 2)
                user.staffs.profile_pic=profile_pic_url
                user.staffs.address=address
                user.save()
                return HttpResponseRedirect('/Manage_Staff/')

def Add_Course(request):
    if request.user != None:
        if request.user.user_type == '1':
            return render(request, 'add_courses.html', {'name':request.user.username})

def add_course_Save(request):
    if request.user != None:
        if request.user.user_type == '1':
            if request.method != 'POST':
                return HttpResponse("Method Not Allowed")
            else:
                course = request.POST.get("new_course")
                course_model = Courses(course_name = course)
                course_model.save()
                return HttpResponseRedirect('/Manage_Course/')

def Add_Student(request):
    if request.user != None:
        if request.user.user_type == '1':
            courses = Courses.objects.all()
            return render(request, 'add_student.html', {'courses':courses, 'name':request.user.username})

def add_student_save(request):
    if request.user != None:
        if request.user.user_type == '1':
            if request.method != 'POST':
                return HttpResponse("Method Not Allowed")
            else:
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                username = request.POST.get('username')
                password = request.POST.get('password')
                address = request.POST.get('address')
                profile_pic = request.POST.get('profile_pic')
                session_start = request.POST.get('session_start')
                session_end = request.POST.get('session_end')
                gender = request.POST.get('gender')
                course_id = request.POST.get('course')
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name,profile_pic)
                profile_pic_url = fs.url(filename)
                user = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password, user_type = 3)
                user.students.address=address
                course_obj = Courses.objects.get(id = course_id)
                user.students.course_id=course_obj
                #start_date = datetime.datetime.strptime(session_start, '%d-%m-%y').strftime('%y-%m-%d')
                #end_date = datetime.datetime.strptime(session_end, '%d-%m-%y').strftime('%y-%m-%d')
                user.students.session_start_year=session_start
                user.students.session_end_year=session_end
                user.students.gender=gender
                user.students.profile_pic=profile_pic_url
                user.save()
                return HttpResponseRedirect('/Manage_Student/')

def Add_Subject(request):
    if request.user != None:
        if request.user.user_type == '1':
            courses=Courses.objects.all()
            staffs=CustomUser.objects.filter(user_type=2)
            context={'staffs':staffs, 'courses':courses, 'name':request.user.username}
            return render(request, 'add_subject.html', context)

def add_subject_save(request):
    if request.user != None:
        if request.user.user_type == '1':
            if request.method != 'POST':
                return HttpResponse("Method Not Allowed")
            else:
                new_subject=request.POST.get('new_subject')
                staff_id=request.POST.get('staff')
                staff=CustomUser.objects.get(id=staff_id)
                course_id=request.POST.get('course')
                course=Courses.objects.get(id=course_id)
                print(staff)
                print(course)
                subject=Subjects(subject_name=new_subject, course_id=course, staff_id=staff)
                subject.save()
                return HttpResponseRedirect('/Manage_Subject/')

def Manage_Student(request):
    if request.user != None:
        if request.user.user_type == '1':
            students = Students.objects.all()
            context = {
                'students':students,
                'name':request.user.username
            }
            return render(request, 'manage_student.html', context)

def Manage_Course(request):
    if request.user != None:
        if request.user.user_type == '1':
            courses = Courses.objects.all()
            context = {
                'courses':courses,
                'name':request.user.username,
            }
            return render(request, 'courses.html', context)

def Manage_Subject(request):
    if request.user != None:
        if request.user.user_type == '1':
            subjects = Subjects.objects.all()
            context = {
                'subjects':subjects,
                'name':request.user.username,
            }
            return render(request, 'manage_subject.html', context)