from django import forms
from  django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from  .models import  Project_Ideas
class CustRegiForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]
class Login_form(forms.Form):
    Email=forms.CharField(required=True,widget= forms.TextInput(attrs={'placeholder':'Enter Email '}))
    password = forms.CharField(max_length=32,required=True,widget=forms.PasswordInput(attrs={"placeholder":"Enter Password"}))

class Hash_form(forms.Form):
    key=forms.CharField(max_length=64,widget=forms.TextInput(attrs={"placeholder":"Enter Receivied Secret Key"}))

####### Password_REST


class Reset_form(forms.Form):
    Username=forms.EmailField(required=True,widget= forms.EmailInput(attrs={'placeholder':'Ex. youremail@gmail.com'}))
class Project_form(forms.Form):
    pro_form_title=forms.CharField(label="Project Title", widget= forms.TextInput(attrs={'placeholder':'Ex. Object detection'}))
    Project_Email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'placeholder': 'Ex. youremail@gmail.com'}))
    Project_Description=forms.CharField(required=1,widget=forms.Textarea(attrs={'placeholders':"Describe about Project , Tools and Technologies",'rows':4, 'cols':15}))
# widgets = {
#           'summary': forms.Textarea(attrs={'rows':4, 'cols':15}),
#         }

class update_profile(forms.Form):
    username = forms.CharField(label="username", widget=forms.TextInput(),max_length=100)
    Email = forms.EmailField(required=True,
                                     widget=forms.EmailInput())
    # password = forms.CharField(label="password", widget=forms.PasswordInput())


