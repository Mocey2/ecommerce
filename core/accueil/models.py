# accueil/models.py

from django.db import models

class HeroSection(models.Model):
    titre_principal = models.CharField(max_length=255)
    texte_bouton_1 = models.CharField(max_length=100)
    texte_bouton_2 = models.CharField(max_length=100)
    image_background = models.ImageField(upload_to='hero/', blank=True, null=True)

    def __str__(self):
        return f"Bannière : {self.titre_principal}"


class IntroCard(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.titre


class AboutSection(models.Model):
    sous_titre = models.CharField(max_length=100, default="Since 1905")
    titre = models.CharField(max_length=255)
    paragraphe_1 = models.TextField()
    paragraphe_2 = models.TextField()
    nombre_annees = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='about/', blank=True, null=True)

    def __str__(self):
        return f"A propos : {self.titre}"


class Temoignage(models.Model):
    nom = models.CharField(max_length=100)
    poste = models.CharField(max_length=100)
    message = models.TextField()
    photo = models.ImageField(upload_to='temoignages/')
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_ajout']

    def __str__(self):
        return f"{self.nom} - {self.poste}"


class TemoignageSection(models.Model):
    image_fond = models.ImageField(upload_to='temoignage_background/', help_text="Image de fond pour la section témoignage")

    def __str__(self):
        return "Image de fond - Section Témoignage"

