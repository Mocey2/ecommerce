"""
Tests unitaires pour les modèles de l'application produit
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from produit.models import CategorieProduit, Produit, Panier, ItemPanier, ProduitHeader

User = get_user_model()


class CategorieProduitModelTest(TestCase):
    """Tests pour le modèle CategorieProduit"""

    def test_creation_categorie(self):
        """Test de création d'une catégorie"""
        categorie = CategorieProduit.objects.create(nom="Électronique")
        self.assertEqual(categorie.nom, "Électronique")
        self.assertEqual(str(categorie), "Électronique")

    def test_categorie_unique(self):
        """Test que les catégories peuvent avoir le même nom (pas de contrainte unique)"""
        CategorieProduit.objects.create(nom="Test")
        # Devrait pouvoir créer une autre avec le même nom
        categorie2 = CategorieProduit.objects.create(nom="Test")
        self.assertEqual(CategorieProduit.objects.filter(nom="Test").count(), 2)


class ProduitModelTest(TestCase):
    """Tests pour le modèle Produit"""

    def setUp(self):
        """Préparation des données de test"""
        self.user = User.objects.create_user(
            email='vendeur@test.com',
            prenom='Test',
            nom='Vendeur',
            password='test123'
        )
        self.categorie = CategorieProduit.objects.create(nom="Électronique")

    def test_creation_produit_minimal(self):
        """Test de création d'un produit avec données minimales"""
        produit = Produit.objects.create(
            nom="Test Produit",
            prix=Decimal('99.99'),
            presentation="Présentation courte",
            description="Description détaillée",
            fabricant="Fabricant Test",
            categorie=self.categorie,
            vendeur=self.user,
            stock=10
        )
        self.assertEqual(produit.nom, "Test Produit")
        self.assertIsNotNone(produit.slug)
        self.assertEqual(produit.slug, "test-produit")

    def test_slug_auto_generation(self):
        """Test de la génération automatique du slug"""
        produit = Produit.objects.create(
            nom="Produit Avec Espaces",
            prix=Decimal('50.00'),
            presentation="Test",
            description="Test",
            fabricant="Test",
            categorie=self.categorie,
            stock=5
        )
        self.assertEqual(produit.slug, "produit-avec-espaces")

    def test_slug_unique_conflict(self):
        """Test que les slugs sont rendus uniques en cas de conflit"""
        Produit.objects.create(
            nom="Même Nom",
            prix=Decimal('10.00'),
            presentation="Test",
            description="Test",
            fabricant="Test",
            categorie=self.categorie,
            stock=1
        )
        produit2 = Produit.objects.create(
            nom="Même Nom",
            prix=Decimal('20.00'),
            presentation="Test",
            description="Test",
            fabricant="Test",
            categorie=self.categorie,
            stock=1
        )
        self.assertEqual(produit2.slug, "meme-nom-2")

    def test_est_en_promo(self):
        """Test de la méthode est_en_promo"""
        # Produit sans promo
        produit1 = Produit.objects.create(
            nom="Sans Promo",
            prix=Decimal('100.00'),
            presentation="Test",
            description="Test",
            fabricant="Test",
            categorie=self.categorie,
            stock=1
        )
        self.assertFalse(produit1.est_en_promo())

        # Produit avec promo
        produit2 = Produit.objects.create(
            nom="Avec Promo",
            prix=Decimal('100.00'),
            prix_promo=Decimal('80.00'),
            presentation="Test",
            description="Test",
            fabricant="Test",
            categorie=self.categorie,
            stock=1
        )
        self.assertTrue(produit2.est_en_promo())

        # Produit avec prix_promo >= prix (pas vraiment une promo)
        produit3 = Produit.objects.create(
            nom="Fausse Promo",
            prix=Decimal('100.00'),
            prix_promo=Decimal('100.00'),
            presentation="Test",
            description="Test",
            fabricant="Test",
            categorie=self.categorie,
            stock=1
        )
        self.assertFalse(produit3.est_en_promo())

    def test_produit_sans_image(self):
        """Test qu'un produit peut être créé sans images"""
        produit = Produit.objects.create(
            nom="Sans Image",
            prix=Decimal('50.00'),
            presentation="Test",
            description="Test",
            fabricant="Test",
            categorie=self.categorie,
            stock=1
        )
        self.assertFalse(produit.image_liste)
        self.assertFalse(produit.image_banniere)

    def test_produit_approbation_defaut(self):
        """Test que l'approbation est False par défaut"""
        produit = Produit.objects.create(
            nom="Test",
            prix=Decimal('10.00'),
            presentation="Test",
            description="Test",
            fabricant="Test",
            categorie=self.categorie,
            stock=1
        )
        self.assertFalse(produit.approuve)
        self.assertFalse(produit.rejete)


class PanierModelTest(TestCase):
    """Tests pour le modèle Panier"""

    def setUp(self):
        """Préparation des données de test"""
        self.user = User.objects.create_user(
            email='client@test.com',
            prenom='Client',
            nom='Test',
            password='test123'
        )
        self.categorie = CategorieProduit.objects.create(nom="Test")
        self.produit1 = Produit.objects.create(
            nom="Produit 1",
            prix=Decimal('50.00'),
            presentation="Test",
            description="Test",
            fabricant="Test",
            categorie=self.categorie,
            stock=10
        )
        self.produit2 = Produit.objects.create(
            nom="Produit 2",
            prix=Decimal('30.00'),
            prix_promo=Decimal('25.00'),
            presentation="Test",
            description="Test",
            fabricant="Test",
            categorie=self.categorie,
            stock=5
        )

    def test_creation_panier(self):
        """Test de création d'un panier"""
        panier = Panier.objects.create(utilisateur=self.user)
        self.assertEqual(panier.statut, 'en_attente_confirmation')
        self.assertEqual(str(panier), f"Panier #{panier.id} - {self.user}")

    def test_panier_vide_total_zero(self):
        """Test que le total d'un panier vide est 0"""
        panier = Panier.objects.create(utilisateur=self.user)
        self.assertEqual(panier.total(), 0)

    def test_panier_avec_items_total(self):
        """Test du calcul du total avec des items"""
        panier = Panier.objects.create(utilisateur=self.user)
        ItemPanier.objects.create(panier=panier, produit=self.produit1, quantite=2)
        ItemPanier.objects.create(panier=panier, produit=self.produit2, quantite=1)

        # Total = (50 * 2) + (25 * 1) = 125
        self.assertEqual(panier.total(), Decimal('125.00'))


class ItemPanierModelTest(TestCase):
    """Tests pour le modèle ItemPanier"""

    def setUp(self):
        """Préparation des données de test"""
        self.user = User.objects.create_user(
            email='client@test.com',
            prenom='Client',
            nom='Test',
            password='test123'
        )
        self.categorie = CategorieProduit.objects.create(nom="Test")
        self.produit = Produit.objects.create(
            nom="Produit Test",
            prix=Decimal('100.00'),
            prix_promo=Decimal('80.00'),
            presentation="Test",
            description="Test",
            fabricant="Test",
            categorie=self.categorie,
            stock=10
        )
        self.panier = Panier.objects.create(utilisateur=self.user)

    def test_creation_item_panier(self):
        """Test de création d'un item dans le panier"""
        item = ItemPanier.objects.create(
            panier=self.panier,
            produit=self.produit,
            quantite=3
        )
        self.assertEqual(item.quantite, 3)
        self.assertEqual(str(item), f"{self.produit.nom} x 3")

    def test_prix_unitaire_avec_promo(self):
        """Test que le prix unitaire utilise le prix promo si disponible"""
        item = ItemPanier.objects.create(
            panier=self.panier,
            produit=self.produit,
            quantite=1
        )
        self.assertEqual(item.prix_unitaire(), Decimal('80.00'))

    def test_prix_unitaire_sans_promo(self):
        """Test que le prix unitaire utilise le prix normal sans promo"""
        produit_sans_promo = Produit.objects.create(
            nom="Sans Promo",
            prix=Decimal('50.00'),
            presentation="Test",
            description="Test",
            fabricant="Test",
            categorie=self.categorie,
            stock=5
        )
        item = ItemPanier.objects.create(
            panier=self.panier,
            produit=produit_sans_promo,
            quantite=1
        )
        self.assertEqual(item.prix_unitaire(), Decimal('50.00'))

    def test_total_item(self):
        """Test du calcul du total d'un item"""
        item = ItemPanier.objects.create(
            panier=self.panier,
            produit=self.produit,
            quantite=4
        )
        # Total = 80 * 4 = 320
        self.assertEqual(item.total(), Decimal('320.00'))


class ProduitHeaderModelTest(TestCase):
    """Tests pour le modèle ProduitHeader"""

    def test_creation_header(self):
        """Test de création d'un header"""
        header = ProduitHeader.objects.create(
            titre="Nos Produits",
            sous_titre="Accueil > Produits"
        )
        self.assertEqual(header.titre, "Nos Produits")
        self.assertEqual(str(header), "Bannière de la page Produits")

    def test_header_valeurs_par_defaut(self):
        """Test des valeurs par défaut"""
        header = ProduitHeader.objects.create()
        self.assertEqual(header.titre, "Produits")
        self.assertEqual(header.sous_titre, "Home > Products")
