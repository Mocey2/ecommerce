from django.contrib import admin
from .models import AboutHeader, AboutCounter

@admin.register(AboutHeader)
class AboutHeaderAdmin(admin.ModelAdmin):
    list_display = ("titre", "sous_titre")

@admin.register(AboutCounter)
class AboutCounterAdmin(admin.ModelAdmin):
    list_display = ("titre", "valeur")