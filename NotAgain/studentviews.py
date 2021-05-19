from django.shortcuts import render, redirect
from django.http import  HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from .forms import Bookform
from .forms import Assignmentform
from .models import Assignment_Submit, CustomUser, Students, Study_materials_upload
from .models import Assignment_upload, Assignment_form, Assignment_Return, Assignment_Submit

def Study_Material_View(request):
    if request.user != None:
        if request.user.user_type == '3':
            #staff_id = request.user.id
            #staff=CustomUser.objects.get(id=staff_id)
            #notes = Study_materials_upload.object.filter(staff_id=staff)
            notes = Study_materials_upload.object.all()
            return render(request, 'study_material_view.html', {'notes': notes, 'name': request.user.first_name})

def timetable(request):
    if request.user != None:
        if request.user.user_type == '3':
            return render(request, 'timetable.html', {'name': request.user.first_name})

def Assignment_View(request):
    if request.user != None:
        if request.user.user_type == '3':
            assign = Assignment_form.object.all()
            return render(request, 'assignment_view.html', {'assign':assign, 'name': request.user.first_name})

def Assignment_Return(request, id):
    if request.user != None:
        if request.user.user_type == '3':
            return render(request, 'assignment_return.html', {'id':id, 'name': request.user.first_name})

def Assignment_Return_Save(request, id):
    if request.method == 'POST':
        assign = Assignment_form.object.get(id=id)
        print(assign.title)
        student_id = request.user.id
        student = CustomUser.objects.get(id=student_id)
        print(student)
        name = request.POST.get('title')
        assign_file = request.FILES['assign_file']
        fs = FileSystemStorage()
        filename = fs.save(assign_file.name, assign_file)
        assign_file_url = fs.url(filename)
        assreturn = Assignment_Submit(student_id=student, assign_form = assign,  name=name)
        assreturn.reference_file = assign_file_url
        assreturn.save()
        return HttpResponseRedirect('/Assignment_View/')
            

def profile(request):
    if request.user != None:
        if request.user.user_type == '3':
            id = request.user.id
            data = Students.objects.get(admin_id=id)
            # print(data.course_id.course_name)
            return render(request, 'profile.html', {'name': request.user.first_name, 'data':data,'profile_pic':data.profile_pic})
