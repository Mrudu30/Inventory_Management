from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.db import IntegrityError
from .forms import edit_user_form

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
        
def edit_user(request,pk):
    user = User.objects.get(id=pk)  
    form = edit_user_form(instance=user)
    
    if request.method == 'POST':
        form = edit_user_form(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        
    context = {'user':user,'form':form}
    return render(request,'profile/signup.html',context)    