from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib import messages
from cloudinary.models import CloudinaryField

# Create your views here.
def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    context = {
        'form':form,
    }
    return render(request, 'registration/register.html', context)

def home(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
    else:
        form = CategoryForm()
    try:
        categories = Category.objects.all()
    except Category.DoesNotExist:
        categories = None
    params = {
        'categories': categories,
        'form': form,
    }

    return render(request, 'index.html', params)

def profile(request, username):
    try:
        user = User.objects.get(pk = username)
        profile = UserProfile.objects.get(user = user)
        units = Unit.get_user_units(profile.id)
        units_count = units.count()
    except Unit.DoesNotExist:
        units = None
    return render(request, 'profile.html',{'units': units, 'count': units_count})
    
def update_profile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        edit_form = EditProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('profile', user.id)
    else:
        edit_form = EditProfileForm(instance=request.user.userprofile) 
    context = {
        'profile_form': edit_form,
    }           
    return render(request, 'edit_profile.html',context)

@login_required(login_url='/accounts/login/')
def add_unit(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        form = UnitsForm(request.POST, request.FILES)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.category = category
            unit.user = request.user.userprofile
            unit.save()
            return redirect('home')
    else:
        form = UnitsForm()
    return render(request, 'bookunit.html', {'form': form})

@login_required(login_url='/accounts/login/')
def units_info(request, category_id, username):
    try:
        user = UserProfile.objects.get(user=username)
        category = Category.objects.get(id=category_id)
        units = Unit.objects.filter(user=user,category=category)
        unit_count = units.count()
    except unit.DoesNotExist:
        units = None

    
    params = {
        'units': units, 
        'count': unit_count,
        
    }   
    return render(request, 'unitsinfo.html', params)


