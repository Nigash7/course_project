from django import forms
from .models import Course
from django.contrib.auth.models import User
from .models import Enrollment, Student, Course

class StudentRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']








class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'video_url']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter course description'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Paste YouTube video link (optional)'
            }),
        }





class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['course']        