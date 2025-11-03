from django.db.models import Sum, F, Q, DecimalField
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import ProduitHeader, Produit, CategorieProduit, Panier, ItemPanier
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse


def produit_list_view(request):
    header = ProduitHeader.objects.first()
    produits = Produit.objects.select_related('categorie').filter(approuve=True).order_by('-date_ajout')
    categories = CategorieProduit.objects.all()
    categorie_filtre = request.GET.get('categorie')

    if categorie_filtre:
        produits = produits.filter(categorie__nom=categorie_filtre)

    paginator = Paginator(produits, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'produit/produit.html', {
        'header': header,
        'categories': categories,
        'produits': page_obj,
    })

def produit_detail_view(request, slug):
    produit = get_object_or_404(Produit, slug=slug, approuve=True)
    return render(request, 'produit/product-single.html', {
        'produit': produit,
    })

@login_required
def ajouter_au_panier(request, slug):
    print("Slug reçu :", slug)
    produit = get_object_or_404(Produit, slug=slug)
    panier, created = Panier.objects.get_or_create(utilisateur=request.user, statut="en_attente_confirmation")

    item, created = ItemPanier.objects.get_or_create(panier=panier, produit=produit)
    if not created:
        item.quantite += 1
    item.save()
    return redirect('panier')

@login_required
def panier_view(request):
    header = ProduitHeader.objects.first()
    panier = Panier.objects.filter(utilisateur=request.user, statut='en_attente_confirmation').first()
    categories = CategorieProduit.objects.all()
    return render(request, 'produit/panier.html', {
        'panier': panier,
        'header': header,
        'categories': categories,
    })


@login_required
def checkout_view(request):
    header = ProduitHeader.objects.first()
    panier = Panier.objects.filter(utilisateur=request.user, statut='en_attente_confirmation').first()
    return render(request, 'produit/checkout.html', {
        'panier': panier,
        'header': header,
    })

@login_required
def valider_commande(request):
    panier = Panier.objects.filter(utilisateur=request.user, statut="en_attente_confirmation").first()

    if panier and panier.items.exists():
        for item in panier.items.all():
            produit = item.produit
            produit.stock -= item.quantite
            produit.save()

        panier.statut = "confirme"
        panier.save()

        Panier.objects.get_or_create(utilisateur=request.user, statut="en_attente_confirmation")

        messages.success(request, "Votre commande a été validée avec succès.")
        return redirect('commande-confirmation')
    else:
        messages.warning(request, "Aucun panier à valider.")
        return redirect('panier')


@login_required
def supprimer_item_panier(request, slug):
    produit = get_object_or_404(Produit, slug=slug)
    panier = Panier.objects.filter(utilisateur=request.user, statut="en_attente_confirmation").first()

    if panier:
        item = panier.items.filter(produit=produit).first()
        if item:
            item.delete()
            messages.success(request, f"{produit.nom} a été retiré du panier.")

    return redirect('panier')

@login_required
def ajouter_produit_vendeur(request):

    if getattr(request.user, "role", None) != "vendeur" and not getattr(request.user, "is_admin", False):
        messages.error(request, "Accès réservé aux vendeurs.")
        return redirect("produits")

    categories = CategorieProduit.objects.all()

    if request.method == "POST":
        nom = request.POST.get("nom", "").strip()
        prix = request.POST.get("prix", "").strip()
        prix_promo = request.POST.get("prix_promo") or None
        presentation = request.POST.get("presentation", "").strip()
        description = request.POST.get("description", "").strip()
        fabricant = request.POST.get("fabricant", "").strip()
        categorie_id = request.POST.get("categorie")
        stock = request.POST.get("stock", "0")

        image_liste = request.FILES.get("image_liste")
        image_banniere = request.FILES.get("image_banniere")

        if not (nom and prix and image_liste and image_banniere and categorie_id):
            messages.error(request, "Merci de remplir tous les champs obligatoires.")
            return render(request, "produit/Ajouter_produit.html", {"categories": CategorieProduit.objects.all()})

        try:
            cat = CategorieProduit.objects.get(id=categorie_id)
        except CategorieProduit.DoesNotExist:
            messages.error(request, "Catégorie invalide.")
            return render(request, "produit/Ajouter_produit.html", {"categories": CategorieProduit.objects.all()})

        produit = Produit(
            nom=nom,
            image_liste=image_liste,
            image_banniere=image_banniere,
            prix=prix,
            prix_promo=prix_promo,
            presentation=presentation,
            description=description,
            fabricant=fabricant,
            categorie=cat,
            stock=stock,
            vendeur=request.user,
        )
        produit.save()
        messages.success(request, "Produit ajouté. En attente d'approbation par l'administrateur.")
        return redirect("liste-produit-vendeur")

    return render(request, "produit/Ajouter_produit.html", {"categories": CategorieProduit.objects.all()})

@login_required
def liste_produit_vendeur(request):
    if getattr(request.user, "role", None) != "vendeur" and not getattr(request.user, "is_admin", False):
        messages.error(request, "Accès réservé aux vendeurs.")
        return redirect("produits")

    produits = (
        Produit.objects.filter(vendeur=request.user)
        .annotate(
            # total des quantités vendues, sur paniers confirmés
            nb_commandes=Sum(
                "itempanier__quantite",
                filter=Q(itempanier__panier__statut="confirme"),
                default=0,
            ),
            total_ventes=Sum(
                F("itempanier__quantite") * Coalesce(F("prix_promo"), F("prix")),
                filter=Q(itempanier__panier__statut="confirme"),
                output_field=DecimalField(max_digits=12, decimal_places=2),
                default=0,
            ),
        )
        .order_by("-date_ajout")
    )

    return render(request, "produit/Liste_produit_vendeur.html", {"produits": produits})

@login_required
def admin_approbations_view(request):
    if not getattr(request.user, "is_admin", False):
        messages.error(request, "Accès réservé à l’administrateur.")
        return redirect("produits")

    en_attente = (Produit.objects
                  .select_related("categorie", "vendeur")
                  .filter(approuve=False, rejete=False)  # 👈 change ici
                  .order_by("-date_ajout"))

    approuves = (Produit.objects
                 .select_related("categorie", "vendeur")
                 .filter(approuve=True)
                 .order_by("-date_ajout")[:20])

    rejetes = (Produit.objects
               .select_related("categorie", "vendeur")
               .filter(rejete=True)
               .order_by("-date_ajout")[:20])

    return render(request, "produit/approuve.html", {
        "en_attente": en_attente,
        "approuves": approuves,
        "rejetes": rejetes,
    })
@login_required
@require_POST
def admin_approuver_produit(request, pk):
    if not getattr(request.user, "is_admin", False):
        messages.error(request, "Accès réservé à l’administrateur.")
        return redirect("produits")

    produit = get_object_or_404(Produit, pk=pk)
    produit.approuve = True
    produit.rejete = False
    produit.save()
    messages.success(request, f"« {produit.nom} » a été approuvé.")
    return redirect("admin-approbations")

@login_required
@require_POST
def admin_rejeter_produit(request, pk):
    if not getattr(request.user, "is_admin", False):
        messages.error(request, "Accès réservé à l’administrateur.")
        return redirect("produits")

    produit = get_object_or_404(Produit, pk=pk)
    produit.approuve = False
    produit.rejete = True
    produit.save()
    messages.warning(request, f"« {produit.nom} » a été rejeté.")
    return redirect("admin-approbations")