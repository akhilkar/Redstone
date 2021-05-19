from django import forms

from .models import Study_materials_upload
from .models import Assignment_upload
from .models import Students, Staffs


class Bookform(forms.ModelForm):
    class Meta:
        model = Study_materials_upload
        fields = ('id','subject', 'title', 'description', 'notes_file')


class Assignmentform(forms.ModelForm):
    class Meta:
        model = Assignment_upload
        fields = ('subject', 'title', 'upload_date', 'description', 'reference_file')

