
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user','email']

class HoodForm(forms.ModelForm):
    class Meta:
        model = Neighbourhood
        exclude = ['admin']

class PostForm(forms.ModelForm):
    CATEGORIES = (
        ('', 'Select a Category'),
        ('Event Alert','Alert'),
        ('Meeting Announcement','Announcement'),
        ('General','General'),
       
    )    
    category = forms.ChoiceField(choices=CATEGORIES,widget=forms.Select())

    class Meta:
        model = Post
        exclude = ['user', 'neighbourhood']

class BusinessForm(forms.ModelForm):
     
    class Meta:
            model = Business
            fields=('name','phone','email','category')
            widgets={
                'name':forms.TextInput(attrs={'placeholder':'Enter Business Title'}) ,
                'phone':forms.TextInput(attrs={'placeholder':'Enter Contact Detail'}),
                'email':forms.TextInput(attrs={'placeholder':'Enter Email Address of business'}),
                # 'category':forms.Select(attrs={'placeholder':'Select Category'}),
            }

class AmenityForm(forms.ModelForm):
    CATEGORIES = (
      ('', 'Select a Category'),
      ('Hospital','Hospital'),
      ('Police','Police'),
      ('Park','Park'),
      ('School','School'),
      ('Fire Department', 'Fire Department')
   )
    amenity_type = forms.ChoiceField(choices=CATEGORIES,widget=forms.Select())
    class Meta:
      model = Amenity
      fields = ['name','phone','email','amenity_type']

class CommentForm(forms.ModelForm):
    class Meta:
      model = Comment
      fields = ['comment']