from django.db import models

class InformationsSite(models.Model):
    nom_site = models.CharField(max_length=100, default="Liquor Store")
    slogan = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    facebook_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    dribbble_link = models.URLField(blank=True, null=True)

    adresse = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom_site} - Informations"

    class Meta:

        verbose_name = "Information du Site"
        verbose_name_plural = "Informations du Site"
