from django.shortcuts import render
from .models import AboutHeader, AboutCounter
from accueil.models import IntroCard, AboutSection, Temoignage, TemoignageSection
from produit.models import Produit


def about_view(request):
    header = AboutHeader.objects.first()
    cards = IntroCard.objects.all()
    about = AboutSection.objects.first()
    produits = Produit.objects.filter(stock__gt=0).order_by('-date_ajout')[:8]
    temoignages = Temoignage.objects.all()[:10]
    temoignage_bg = TemoignageSection.objects.first()
    counters = AboutCounter.objects.all()


    return render(request, "about/about.html",
    {
        "header": header,
        'cards': cards,
        'about': about,
        'produits': produits,
        'temoignages': temoignages,
        'temoignage_bg': temoignage_bg,
        "counters": counters
    })
