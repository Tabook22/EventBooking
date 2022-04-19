from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegisterUserForm

#Logout ----------------------------------------------------
def logout_user(request):
    logout(request)
    messages.success(request,("You are Logged out of the system !!!"))
    return redirect('home')

#Login -----------------------------------------------------
def login_user(request):
    #Check to see if the user filled in the login page
    if request.method =="POST":
        username=request.POST['username']
        password=request.POST['password']

        #Check to see if the user exist or not
        user=authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            #Redirect the a success page.
            return redirect('home')
        else:
            #Return an 'invalid login' error message
            messages.success(request,("There is an error, check your username and password"))
            return redirect('login')
    else:
        return render(request, 'members/login.html', {})

#Register
def register_user(request):
    if request.method=="POST":
        form=RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1'] #password1, because in the form we have two password to make sure the user entered the correct password (comparing password1, and 2)
            user=authenticate (username=username, password=password)
            #login with the new username and password
            login(request, user) #Going to the function login above
            messages.success(request,("Registration was Successful!!!"))
            return redirect('home')

    else:
        form=RegisterUserForm()

    return render(request, 'members/register_user.html',{'form':form})
