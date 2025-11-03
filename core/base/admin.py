from django.contrib import admin
from .models import InformationsSite

@admin.register(InformationsSite)
class InformationsSiteAdmin(admin.ModelAdmin):
    list_display = ('nom_site', 'email', 'telephone', 'updated_at')
    fieldsets = (
        ("Informations générales", {
            'fields': ('nom_site', 'slogan', 'description')
        }),
        ("Réseaux sociaux", {
            'fields': ('facebook_link', 'twitter_link', 'instagram_link', 'dribbble_link')
        }),
        ("Contact", {
            'fields': ('adresse', 'telephone', 'email')
        }),
    )
