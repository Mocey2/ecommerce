# produit/urls.py

from django.urls import path
from django.views.generic import TemplateView
from .views import (produit_list_view, produit_detail_view, ajouter_au_panier, panier_view, checkout_view,
                    valider_commande, supprimer_item_panier, ajouter_produit_vendeur, liste_produit_vendeur,
                    admin_approbations_view, admin_approuver_produit, admin_rejeter_produit)

urlpatterns = [
    path('', produit_list_view, name='produits'),

    # --- Espace vendeur ---
    path('vendeur/ajouter/', ajouter_produit_vendeur, name='ajouter-produit-vendeur'),
    path('vendeur/mes-produits/', liste_produit_vendeur, name='liste-produit-vendeur'),

    # --- Espace administrateur : approbations ---
    path('admin/approbations/', admin_approbations_view, name='admin-approbations'),
    path('admin/approbations/<int:pk>/approuver/', admin_approuver_produit, name='admin-approbation-approuver'),
    path('admin/approbations/<int:pk>/rejeter/', admin_rejeter_produit, name='admin-approbation-rejeter'),


    # --- Panier & commande ---
    path('ajouter-au-panier/<slug:slug>/', ajouter_au_panier, name='panier-ajout'),
    path('panier/supprimer/<slug:slug>/', supprimer_item_panier, name='supprimer-item-panier'),
    path('valider-commande/', valider_commande, name='valider-commande'),
    path('commande-confirmation/', TemplateView.as_view(template_name="produit/confirmation.html"),
         name='commande-confirmation'),
    path('panier/', panier_view, name='panier'),
    path('checkout/', checkout_view, name='checkout'),

    # Toujours en dernier :
    path('<slug:slug>/', produit_detail_view, name='produit-detail'),
]
