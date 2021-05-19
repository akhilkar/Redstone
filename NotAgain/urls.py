"""newtest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from NotAgain import studentviews
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views, hodviews, staffviews
from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name="login"),
    path('logout/',views.logout_view, name="logout"),
    #path('Add_Student/', hodviews.Add_Student),
    path('Manage_Staff/Add_Staff/', hodviews.Add_Staff),
    path('Manage_Staff/', hodviews.Manage_Staff),
    path('Manage_Student/', hodviews.Manage_Student),
    path('Add_Staff_Save/', hodviews.add_staff_Save),
    path('Manage_Course/', hodviews.Manage_Course),
    path('Manage_Course/Add_Course/', hodviews.Add_Course, name="Add Course"),
    path('Add_Course_Save/', hodviews.add_course_Save),
    path('Manage_Subject/', hodviews.Manage_Subject),
    path('Manage_Subject/Add_Subject/', hodviews.Add_Subject),
    path('Add_Subject_Save/', hodviews.add_subject_save),
    path('Add_Student_Save/', hodviews.add_student_save),
    path('Manage_Student/Add_Student/', hodviews.Add_Student),
    path('HOD_Dashboard/', views.HOD_Dashboard, name="Dashboard"),
    path('doLogin/', views.login_auth),
    path('Staff_Dashboard/', views.Staff_Dashboard),
    path('Staff_Timetable/', staffviews.Staff_TT),
    path('Staff_TT/', staffviews.Staff_timetable),
    path('timetable/', studentviews.timetable, name="timetable"),
    path('Staff_Study_material/', staffviews.Study_Upload, name="Study_material"),
    path('Staff_Study_material/Study_material_upload/', staffviews.Study_material_upload, name="Study_material_upload"),
    path('Study_Material_Save/', staffviews.Study_upload_Save),
    path('Staff_Assignment/', staffviews.Assignment),
    path('Staff_Assignment/Assignment_upload/', staffviews.Assignment_upload),
    path('Assignment_Upload_Save/', staffviews.Assignment_upload_Save),
    path('Dashboard/', views.Dashboard),
    path('Study_Material_View/', studentviews.Study_Material_View),
    path('Assignment_View/', studentviews.Assignment_View),
    path('Assignment_submit/<str:id>', studentviews.Assignment_Return),
    path('Assignment_Response/<str:id>', staffviews.Assignment_Check),
    path('Assignment_Return_Save/<str:id>', studentviews.Assignment_Return_Save),
    path('Student_profile/', studentviews.profile ),
    path('Staff_profile/', staffviews.Profile),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
