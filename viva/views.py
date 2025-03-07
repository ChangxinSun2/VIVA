from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import ShowInfo, Favorite
from django.shortcuts import render

def home(request):
    query = request.GET.get('q')
    if query:
        shows = ShowInfo.objects.filter(
            Q(title__icontains=query) | Q(location__icontains=query) | Q(genre__icontains=query)
        )
    else:
        shows = ShowInfo.objects.all()
    return render(request, 'index.html', {'shows': shows})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def add_favorite(request, show_id):
    show = get_object_or_404(ShowInfo, id=show_id)
    Favorite.objects.get_or_create(user=request.user, show=show)
    return redirect('home')

@login_required
def favorites(request):
    user_favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites.html', {'favorites': user_favorites})

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})
