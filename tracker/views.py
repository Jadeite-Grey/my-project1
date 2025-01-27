# from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Medicine
from .forms import MedicineForm



# Create your views here.


# Home Page
def home(request):
    return render(request, 'tracker/home.html')

# Signup Page
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('account')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})

# Login Page
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('account')
    return render(request, 'tracker/login.html')

# Logout Page
def user_logout(request):
    logout(request)
    return redirect('home')

# Account Page
@login_required
def account(request):
    medicines = Medicine.objects.filter(user=request.user)
    return render(request, 'tracker/account.html', {'medicines': medicines})

# Add Medicine Page
@login_required
def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.user = request.user
            medicine.save()
            return redirect('account')
    else:
        form = MedicineForm()
    return render(request, 'tracker/add_medicine.html', {'form': form})

# Edit Medicine Page
@login_required
def edit_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id, user=request.user)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'tracker/edit_medicine.html', {'form': form})

# Delete Medicine Page
@login_required
def delete_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id, user=request.user)
    medicine.delete()
    return redirect('account')

