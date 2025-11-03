# produit/models.py

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

class ProduitHeader(models.Model):
    titre = models.CharField(max_length=255, default="Produits")
    sous_titre = models.CharField(max_length=255, default="Home > Products")
    image_fond = models.ImageField(upload_to='produits/headers/', blank=True, null=True)

    def __str__(self):
        return f"Bannière de la page Produits"


class CategorieProduit(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    image_liste = models.ImageField(upload_to="produits/liste/")
    image_banniere = models.ImageField(upload_to="produits/banniere/")

    vendeur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="produits", null=True,
                                blank=True)
    approuve = models.BooleanField(default=False)
    rejete = models.BooleanField(default=False)

    prix = models.DecimalField(max_digits=10, decimal_places=2)
    prix_promo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    presentation = models.TextField(help_text="Court texte en haut de page")
    description = models.TextField()
    fabricant = models.TextField()

    categorie = models.ForeignKey(CategorieProduit, on_delete=models.SET_NULL, null=True)
    stock = models.PositiveIntegerField(default=0)

    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

    def est_en_promo(self):
        return self.prix_promo and self.prix_promo < self.prix

    def _build_unique_slug(self):
        base = slugify(self.nom) or "produit"
        slug = base
        i = 1
        Model = self.__class__
        # éviter collision et ignorer soi-même si update
        while Model.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            i += 1
            slug = f"{base}-{i}"
        return slug

    def save(self, *args, **kwargs):
        # Appeler la METHODE d'instance, pas une fonction globale
        if not self.slug:
            self.slug = self._build_unique_slug()
        super().save(*args, **kwargs)

class Panier(models.Model):
    STATUT_CHOICES = [
        ('en_attente_confirmation', 'En attente de confirmation'),
        ('confirme', 'Confirmé'),
    ]

    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente_confirmation')
    date_creation = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.total() for item in self.items.all())

    def __str__(self):
        return f"Panier #{self.id} - {self.utilisateur}"


class ItemPanier(models.Model):
    panier = models.ForeignKey(Panier, related_name="items", on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def prix_unitaire(self):
        return self.produit.prix_promo if self.produit.est_en_promo() else self.produit.prix

    def total(self):
        return self.prix_unitaire() * self.quantite

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"