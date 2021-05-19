from django.shortcuts import render, redirect
from django.http import  HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from .forms import Bookform
from .forms import Assignmentform
from .models import CustomUser, Study_materials_upload, Staffs, Students, Courses, Subjects
from .models import Assignment_upload, Assignment_form, Students, Assignment_Submit

def login(request):
    return render(request, 'login.html')

def HOD_Dashboard(request):
    if request.user != None:
        if request.user.user_type == '1':
            context = {
                'total_staff':Staffs.objects.all().count(),
                'total_student':Students.objects.all().count(),
                'total_course':Courses.objects.all().count(),
                'total_subject':Subjects.objects.all().count(),
                'name':request.user.username,
            }
            return render(request, 'hod_dashboard.html', context)

def Staff_Dashboard(request):
    if request.user != None:
        if request.user.user_type == '2':
            staff_id = request.user.id
            staff = CustomUser.objects.get(id=staff_id)
            print(staff)
            staff = Staffs.objects.get(admin_id=staff.id)
            staff_id = request.user.id
            staff_count=CustomUser.objects.get(id=staff_id)
            assign = Assignment_form.object.filter(staff_id=staff_count).count()
            study = Study_materials_upload.object.filter(staff_id=staff_count).count()
            student = Students.objects.all().count()
            print(staff)
            context = {
                'name': request.user.first_name,
                'profile_pic': staff.profile_pic,
                'assign':assign,
                'study':study,
                'student':student
            }
            return render(request, 'staff_dashboard.html', context)

def Dashboard(request):
    if request.user != None:
        if request.user.user_type == '3':
            id = request.user.id
            print(id)
            context = {
                'name': request.user.first_name,
                'assign': Assignment_form.object.all().count(),
                'study':Study_materials_upload.object.all().count(),
                'assign_submit':Assignment_Submit.object.filter(student_id=id).count(),
            }
            print(Assignment_Submit.object.filter(student_id=id).count())
            return render(request, 'dashboard.html', context)

def login_auth(request):
    if request.method != "POST":
        return HttpResponse("Not allowed")
    else:
        username = request.POST.get("username")
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        if user != None:
            auth_login(request, user)
            #return HttpResponseRedirect("/HOD_Dashboard/")
            type = request.user.user_type
            if type == '1':
                return HttpResponseRedirect('/HOD_Dashboard/')
            elif type == '2':
                return HttpResponseRedirect('/Staff_Dashboard/')
            elif type == '3':
                return HttpResponseRedirect('/Dashboard/')
        if user == None:
            return HttpResponse("Not allowed")


def logout_view(request):
    logout(request)
    return redirect('/')



def test33(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['notes_file']
        fs = FileSystemStorage()
        file = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(file)
    return render(request, 'another one.html', context)


