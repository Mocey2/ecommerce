"""
Tests d'intégration pour les vues de l'application produit
"""
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from produit.models import CategorieProduit, Produit, Panier, ItemPanier, ProduitHeader

User = get_user_model()


class ProduitListViewTest(TestCase):
    """Tests pour la vue liste des produits"""

    def setUp(self):
        """Préparation des données de test"""
        self.client = Client()
        self.url = reverse('produits')

        self.header = ProduitHeader.objects.create(
            titre="Nos Produits",
            sous_titre="Accueil > Produits"
        )

        self.categorie1 = CategorieProduit.objects.create(nom="Électronique")
        self.categorie2 = CategorieProduit.objects.create(nom="Vêtements")

        # Créer quelques produits approuvés
        for i in range(5):
            Produit.objects.create(
                nom=f"Produit {i}",
                prix=Decimal('50.00'),
                presentation="Test",
                description="Test",
                fabricant="Test",
                categorie=self.categorie1,
                stock=10,
                approuve=True
            )

    def test_liste_produits_accessible(self):
        """Test que la page liste des produits est accessible"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_liste_produits_context(self):
        """Test que le contexte contient les bonnes données"""
        response = self.client.get(self.url)
        self.assertIn('produits', response.context)
        self.assertIn('header', response.context)
        self.assertIn('categories', response.context)

    def test_filtre_par_categorie(self):
        """Test du filtrage par catégorie"""
        # Créer un produit dans la catégorie 2
        Produit.objects.create(
            nom="Produit Vêtement",
            prix=Decimal('30.00'),
            presentation="Test",
            description="Test",
            fabricant="Test",
            categorie=self.categorie2,
            stock=5,
            approuve=True
        )

        response = self.client.get(self.url, {'categorie': self.categorie2.id})
        self.assertEqual(response.status_code, 200)
        produits = response.context['produits']

        # Tous les produits doivent être de la catégorie 2
        for produit in produits:
            self.assertEqual(produit.categorie, self.categorie2)

    def test_seuls_produits_approuves_affiches(self):
        """Test que seuls les produits approuvés sont affichés"""
        # Créer un produit non approuvé
        Produit.objects.create(
            nom="Produit Non Approuvé",
            prix=Decimal('100.00'),
            presentation="Test",
            description="Test",
            fabricant="Test",
            categorie=self.categorie1,
            stock=1,
            approuve=False
        )

        response = self.client.get(self.url)
        produits = response.context['produits']

        # Vérifier qu'aucun produit non approuvé n'est dans la liste
        for produit in produits:
            self.assertTrue(produit.approuve)
