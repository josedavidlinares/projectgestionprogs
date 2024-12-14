# views.py en tu aplicación de usuarios

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomAuthenticationForm

def login_view(request):
    form = CustomAuthenticationForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('dashboard')  # Redirigir a una URL específica después de iniciar sesión
    return render(request, 'index.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')  # Redirigir a la página de inicio de sesión después de cerrar sesión
