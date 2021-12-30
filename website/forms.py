from django import forms
from django.contrib.auth.models import User
# from .models import UserProfile

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#     def __init__(self, *args, **kwargs):
#         super(UserForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'

# class UserProfileForm(forms.ModelForm):
#     profile_picture=forms.ImageField(required=False,error_messages={'invalid':("Image files only")},widget=forms.FileInput)
#     class Meta:
#         model = UserProfile
#         fields = ('first_name', 'last_name','phone', 'address_line_1','address_line_2','country','state','city','pin','profile_picture')

#     def __init__(self, *args, **kwargs):
#         super(UserProfileForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'
