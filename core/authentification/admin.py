from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('email', 'prenom', 'nom', 'role', 'is_active', 'is_admin')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Infos', {'fields': ('prenom', 'nom', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'prenom', 'nom', 'password1', 'password2', 'role'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ('is_active', 'is_admin')

admin.site.register(CustomUser, CustomUserAdmin)