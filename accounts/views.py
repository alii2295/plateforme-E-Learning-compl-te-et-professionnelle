from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ce nom d\'utilisateur existe déjà.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Cet email est déjà utilisé.')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        Profile.objects.create(user=user)

        login(request, user)
        messages.success(request, 'Compte créé avec succès!')
        return redirect('home')

    return render(request, 'accounts/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')

    return render(request, 'accounts/login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'Vous êtes déconnecté.')
    return redirect('home')


@login_required
def profile(request):
    profile = request.user.profile
    enrollments = request.user.enrollment_set.all()

    context = {
        'profile': profile,
        'enrollments': enrollments,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()

        profile.bio = request.POST.get('bio')
        profile.phone = request.POST.get('phone')
        profile.location = request.POST.get('location')
        profile.website = request.POST.get('website')

        if request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']

        profile.save()
        messages.success(request, 'Profil mis à jour avec succès!')
        return redirect('profile')

    return render(request, 'accounts/edit_profile.html', {'profile': profile})