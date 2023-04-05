from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MyFileUpload

class MyFileForm(forms.Form):
    # uploader_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','style':'background-color:green','value':'bharath'}))
    uploader_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    file=forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))
    
    
class login_form(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "field",
				
				'autocomplete':"off"

            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "field"
            }
        ))
    

class NewUserForm(UserCreationForm):
	# email = forms.EmailField(required=True)
	# class Meta:
	# 	model = User
	# 	fields = ("username", "password1", "password2")
		
    class Meta:
        model = User
        fields = {
            'username' : forms.TextInput(attrs = {'placeholder': 'Username','style':'background-color:green'}),
            'password1'    : forms.TextInput(attrs = {'placeholder': 'Password-one'}),
            'password2'    : forms.TextInput(attrs = {'placeholder': 'E-Mail'}),
        }
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user