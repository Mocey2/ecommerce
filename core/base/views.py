from django.shortcuts import render

def base(request):
    return render(request, 'base/base.html')  # ou 'base/home.html' si tu crées une homepage distincte
