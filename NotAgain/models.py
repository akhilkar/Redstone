from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Staff"), (3, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

class Study_materials_upload(models.Model):
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length=20, default='', null=True)
    title = models.CharField(max_length=20, default='', null=True)
    description = models.CharField(max_length=200, default='', null=True)
    notes_file = models.FileField(upload_to='media')
    object = models.Manager()


class Assignment_upload(models.Model):
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length=20, default='', null=True)
    title = models.CharField(max_length=20, default='', null=True)
    upload_date = models.DateField()
    description = models.CharField(max_length=200, default='', null=True)
    reference_file = models.FileField(upload_to='media')
    object = models.Manager()

class Assignment_form(models.Model):
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length=20, default='', null=True)
    title = models.CharField(max_length=20, default='', null=True)
    upload_date = models.DateField()
    description = models.CharField(max_length=200, default='', null=True)
    reference_file = models.FileField(upload_to='media')
    object = models.Manager()

class Assignment_Return(models.Model):
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    assign_form = models.OneToOneField(Assignment_form, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default='', null=True)
    reference_file = models.FileField(upload_to='media')
    object = models.Manager()

class Assignment_Submit(models.Model):
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    assign_form = models.ForeignKey(Assignment_form, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default='', null=True)
    reference_file = models.FileField(upload_to='media')
    object = models.Manager() 
    

class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    profile_pic = models.ImageField(upload_to = 'staff_profile_img')
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    profile_pic = models.ImageField(upload_to = 'media/student_profile_img')
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    address = models.TextField()
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class  Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    Student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            Staffs.objects.create(admin=instance)
        if instance.user_type==3:
            Students.objects.create(admin=instance,course_id=Courses.objects.get(id=1), session_start_year='2021-01-01', session_end_year='2023-01-01')

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.staffs.save()
    if instance.user_type==3:
        instance.students.save()