from django.forms import ModelForm
from django import forms
from .models import Comment,Subscribe
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CommentForm(ModelForm):
    
    class Meta:
        model = Comment
        fields = ("content",'name','email','website')

       
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['content'].widget.attrs['placeholder'] = "Type your comment here"
        self.fields['email'].widget.attrs['placeholder'] = "Email "
        self.fields['name'].widget.attrs['placeholder'] = " Name"
        self.fields['website'].widget.attrs['placeholder'] = "Website matra"
        
    #or this can be used instead
    #from django import forms
    #     widgets = {
    #         'content': forms.Textarea(attrs={'placeholder': 'Type your comment here'}),
    #         'email': forms.TextInput(attrs={'placeholder': 'Email'}),
    #         'name': forms.TextInput(attrs={'placeholder': 'Name'}),
    #         'website': forms.TextInput(attrs={'placeholder': 'Website'}),
    #    }
class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = "__all__"
        labels = {'email':_('')}
        widgets ={
            'email': forms.TextInput(attrs={'placeholder':'Enter your email'})
        }

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2')
       
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "Username"
        self.fields['email'].widget.attrs['placeholder'] = "Email "
        self.fields['password1'].widget.attrs['placeholder'] = "Password "
        self.fields['password2'].widget.attrs['placeholder'] = "Confirm Password "

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise forms.ValidationError("Username Already Exists!")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise forms.ValidationError("Email Already Exists !")
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password does not match!')
        return password2


        
        