# produit/admin.py

from django.contrib import admin
from .models import ProduitHeader, Produit, CategorieProduit, Panier, ItemPanier

@admin.register(ProduitHeader)
class ProduitHeaderAdmin(admin.ModelAdmin):
    list_display = ('titre',)

@admin.register(CategorieProduit)
class CategorieProduitAdmin(admin.ModelAdmin):
    list_display = ['nom']

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prix', 'prix_promo', 'categorie', 'stock']
    list_filter = ['categorie']
    readonly_fields = ('slug',)

class ItemPanierInline(admin.TabularInline):
    model = ItemPanier
    extra = 0

@admin.register(Panier)
class PanierAdmin(admin.ModelAdmin):
    list_display = ['id', 'utilisateur', 'statut', 'date_creation']
    list_filter = ['statut']
    inlines = [ItemPanierInline]