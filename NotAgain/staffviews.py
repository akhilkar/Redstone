from django.shortcuts import render, redirect
from django.http import  HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from .models import Assignment_Submit, Courses, CustomUser, Staffs, Subjects, Students
import datetime
from .forms import Bookform
from .forms import Assignmentform
from .models import Study_materials_upload
from .models import Assignment_upload, Assignment_form, Assignment_Submit

def Staff_TT(request):
    if request.user != None:
        if request.user.user_type == '2':
            context = {
                'name': request.user.first_name
            }
            return render(request, 't2_timetable.html', context, {'name': request.user.first_name})

def Staff_timetable(request):
    if request.user != None:
        if request.user.user_type == '2':
            return render(request, 't2_timetable.html')

def Study_Upload(request):
    if request.user != None:
        if request.user.user_type == '2':
            staff_id = request.user.id
            staff=CustomUser.objects.get(id=staff_id)
            notes = Study_materials_upload.object.filter(staff_id=staff)
            return render(request, 'Study_material.html', {'notes': notes, 'name': request.user.first_name})

def Study_material_upload(request):
    if request.user != None:
        if request.user.user_type == '2':
            return render(request, 'Study_material_upload.html',{'name': request.user.first_name})

def Study_upload_Save(request):
    
    if request.method == 'POST':
        staff_id = request.user.id
        staff=CustomUser.objects.get(id=staff_id)
        subject=Subjects.objects.get(staff_id=staff_id)
        Subject = request.POST.get('subject')
        title = request.POST.get('title')
        description = request.POST.get('description')
        notes_file = request.FILES['notes_file']
        fs = FileSystemStorage()
        filename = fs.save(notes_file.name, notes_file)
        notes_file_url = fs.url(filename)
        study = Study_materials_upload(staff_id=staff, subject=subject.subject_name, title=title, description=description)
        study.notes_file=notes_file_url
        study.save()
        return HttpResponseRedirect('/Staff_Study_material/')

def Assignment(request):
    if request.user != None:
        if request.user.user_type == '2':
            staff_id = request.user.id
            staff=CustomUser.objects.get(id=staff_id)
            assign = Assignment_form.object.filter(staff_id=staff)
            print(assign)
            #notes = Assignment_upload.object.filter()
            return render(request, 'Assignment.html', {'assign':assign, 'name': request.user.first_name})
            #else:
            #return render(request, 'Assignment.html')


def Assignment_upload(request):
    if request.user != None:
        if request.user.user_type == '2':
            return render(request, 'Assignment_upload.html',{'name': request.user.first_name})

def Assignment_upload_Save(request):
    if request.method == 'POST':
        staff_id = request.user.id
        staff=CustomUser.objects.get(id=staff_id)
        subject=Subjects.objects.get(staff_id=staff_id)
        Subject = request.POST.get('subject')
        title = request.POST.get('title')
        description = request.POST.get('description')
        reference_file = request.FILES['reference_file']
        fs = FileSystemStorage()
        filename = fs.save(reference_file.name, reference_file)
        reference_file_url = fs.url(filename)
        assign = Assignment_form(staff_id=staff, subject=subject.subject_name, title=title, description=description, upload_date=request.POST.get('date'))
        assign.reference_file=reference_file_url
        assign.save()
        return HttpResponseRedirect('/Staff_Assignment/')

def Assignment_Check(request, id):
    assign = Assignment_Submit.object.filter(assign_form=id)
    print(assign)
    return render(request, 'assignment_check.html', {'assign':assign})

def Profile(request):
    if request.user != None:
        if request.user.user_type == '2':
            id = request.user.id
            data = Staffs.objects.get(admin_id=id)
            context = {
                'data':data
            }
            return render(request, 'staff_profile.html', context)