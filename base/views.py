from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.db import IntegrityError
from . import forms as f
from . import models as m
from django.http import Http404,HttpResponse

# Create your views here.
@login_required(login_url='signin')
def create_inventory(request):
    if request.user:
        user = request.user
        inventory = m.Inventory.objects.filter(user=user).first()
        if inventory is None:
            inventory = m.Inventory.objects.create(user=user, name='My Inventory')
        return redirect('inventory', pk=inventory.id)
    
@login_required(login_url='signin')
def home(request):
    if request.user:
        user = request.user
        inventory = m.Inventory.objects.filter(user=user).first()
        if inventory is None:
            inventory = m.Inventory.objects.create(user=user, name='My Inventory')
        context = {
            'inventory': inventory
        } 
        return render(request, 'base/home.html', context)
    else:
        return render(request,'base/home.html')

# ------ User Profile ------

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
    form = f.edit_user_form(instance=user)
    
    if request.method == 'POST':
        form = f.edit_user_form(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        
    context = {'user':user,'form':form}
    return render(request,'profile/signup.html',context)    

# ------- Inventory Management -------

# inventory showing
@login_required(login_url='signin')
def inventory(request,pk):
    inventory = m.Inventory.objects.get(id=pk)
    products = inventory.products_present.all()
    
    if request.user != inventory.user:
        return Http404()
    else:
        context = {'inventory':inventory,"products":products}
        return render(request,'base/inventory.html',context)

@login_required(login_url='signin')
def edit_inventory(request,pk):
    inventory = get_object_or_404(m.Inventory, id=pk)
    if request.user != inventory.user:
        return Http404()
    else:
        if request.method == 'POST':
            form = f.edit_inventory(request.POST, instance=inventory)
            if form.is_valid():
                form.save()
                return redirect('inventory', pk=inventory.id)
        else:
            form = f.edit_inventory(instance=inventory)
        context = {
            'title': 'Edit Inventory',
            'form': form,
            'inventory': inventory
        }
        return render(request, 'base/form_rendering.html', context)

# ------- Product Management -------

# adding products
@login_required(login_url='signin')
def add_products(request,pk):
    inventory = get_object_or_404(m.Inventory,id=pk)
    if request.user != inventory.user:
        return HttpResponse('User Not Allowed to Change <a href="/">home</a>')
    if request.method == "POST":
        form = f.product_adding(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            inventory.products_present.add(product)
            return redirect('inventory',pk = inventory.id)
    else:
        form = f.product_adding()
    context = {
        'title': 'Add Product',
        'form': form,
        'inventory': inventory
    }
    return render(request, 'base/form_rendering.html', context)