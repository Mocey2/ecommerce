from django.db import models

class AboutHeader(models.Model):
    titre = models.CharField(max_length=255, default="About Us")
    sous_titre = models.CharField(max_length=255, default="Home > About")
    image_fond = models.ImageField(upload_to='about/header/', null=True, blank=True)

    def __str__(self):
        return "Header - À propos"

class AboutCounter(models.Model):
    titre = models.CharField(max_length=100)
    valeur = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.titre} - {self.valeur}"
