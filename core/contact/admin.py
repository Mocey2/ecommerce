from django.contrib import admin
from .models import ContactHeader, ContactMessage, ContactInfo

@admin.register(ContactHeader)
class ContactHeaderAdmin(admin.ModelAdmin):
    list_display = ("titre", "sous_titre")


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('adresse', 'telephone', 'email', 'site_web')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'sujet', 'date_envoi')
    list_filter = ('date_envoi',)
    search_fields = ('nom', 'email', 'sujet')