from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

#Create class and import it or an instance or the UserCreationForm,
#just adding to it the three new things (email,first_name, and last_name)
class RegisterUserForm(UserCreationForm):
    # the email, first name and last name not build in the authenticaiton system, not lile
    # username and passwords, that is why we style them in this way
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    firt_name=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model=User
        fields=('username', 'first_name', 'email', 'password1','password2')

# the username and password are build in the athenticaiton system, that is why
# we have to create a special function for them
    def __init__(self,*args,**kwargs):
        super(RegisterUserForm, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['class']='form-control'