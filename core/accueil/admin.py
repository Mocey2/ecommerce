# accueil/admin.py

from django.contrib import admin
from .models import HeroSection, IntroCard, AboutSection, Temoignage, TemoignageSection

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('titre_principal',)

@admin.register(IntroCard)
class IntroCardAdmin(admin.ModelAdmin):
    list_display = ('titre',)

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('titre', 'nombre_annees')

@admin.register(Temoignage)
class TemoignageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'poste', 'date_ajout')
    search_fields = ('nom', 'poste')


@admin.register(TemoignageSection)
class TemoignageSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_fond')
