from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class usersignup(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']

# class userupdate(forms.ModelForm):
#     email = forms.EmailField()
#     class Meta:
#         model = User
#         fields = ['first_name','last_name','username','email']

# class profileupdate(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['profile_picture','address','contact_no']