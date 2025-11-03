from django.db import models

class ContactHeader(models.Model):
    titre = models.CharField(max_length=255, default="Contact")
    sous_titre = models.CharField(max_length=255, default="Home >")
    image_fond = models.ImageField(upload_to='contact/header/', null=True, blank=True)

    def __str__(self):
        return "Header - Contact"


class ContactInfo(models.Model):
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    site_web = models.URLField()

    def __str__(self):
        return "Informations de contact"

class ContactMessage(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    sujet = models.CharField(max_length=200)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.sujet}"










