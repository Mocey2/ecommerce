# accueil/views.py

from django.shortcuts import render
from .models import HeroSection, IntroCard, AboutSection, Temoignage, TemoignageSection
from produit.models import Produit
from blog.models import Article

def index(request):
    hero = HeroSection.objects.first()
    cards = IntroCard.objects.all()
    about = AboutSection.objects.first()
    produits = Produit.objects.filter(stock__gt=0).order_by('-date_ajout')[:8]
    temoignages = Temoignage.objects.all()[:10]
    temoignage_bg = TemoignageSection.objects.first()
    articles_recents = Article.objects.order_by('-date_publication')[:4]

    return render(request, 'accueil/index.html', {
        'hero': hero,
        'cards': cards,
        'about': about,
        'produits': produits,
        'temoignages': temoignages,
        'temoignage_bg': temoignage_bg,
        'articles_recents': articles_recents,
    })
