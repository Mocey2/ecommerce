0# authentification/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

def register_view(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        role = request.POST.get('role', 'vendeur')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect('register')

        user = CustomUser.objects.create_user(email=email, prenom=prenom, nom=nom, password=password, role=role)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = f"{request.scheme}://{request.get_host()}/authentification/activate/{uid}/{token}/"

        send_mail(
            "Activation de votre compte",
            f"Cliquez sur le lien pour activer votre compte : {activation_link}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        messages.success(request, "Merci de consulter votre adresse mail afin d'activer votre compte avant de vous connecter.")
        return redirect('register')

    return render(request, 'authentification/register.html')

def activate_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Votre compte est activé. Vous pouvez maintenant vous connecter.")
        return redirect('login')
    else:
        messages.error(request, "Lien invalide ou expiré.")
        return redirect('register')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('accueil')
            else:
                messages.error(request, "Merci de bien vouloir activer votre compte")
        else:
            messages.error(request, "Identifiants incorrects")
    return render(request, 'authentification/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
