from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.db import IntegrityError

# Create your views here.
def home(request):
    return render(request,'base/home.html')

@login_required(login_url='signin')
def profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'profile/profile.html', context)

def signup(request):
    if request.method == 'GET':
        return render(request, 'profile/signup.html', 
                       {'form':UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], 
                            password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'profile/signup.html', 
                 {'form':UserCreationForm,
                 'error':'Username already taken. Choose new username.'})
        else:
            return render(request, 'profile/signup.html', 
             {'form':UserCreationForm, 'error':'Passwords do not match'})

def signout(request):        
    logout(request)
    return redirect('home')

def signin(request):    
    if request.method == 'GET':
        return render(request, 'profile/signin.html', 
                      {'form':AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request,'profile/signin.html', 
                    {'form': AuthenticationForm(), 
                    'error': 'username and password do not match'})
        else: 
            login(request,user)
            return redirect('home')