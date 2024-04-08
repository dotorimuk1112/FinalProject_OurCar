from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from common.forms import CustomUserForm  # CustomUserForm을 사용하기 위해 import

def logout_view(request):
    logout(request)
    return redirect('index')

def signup(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)  # CustomUserForm 사용
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserForm()  # CustomUserForm 사용
    return render(request, 'common/signup.html', {'form': form})
