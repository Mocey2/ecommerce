# blog/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BlogHeader(models.Model):
    titre = models.CharField(max_length=255, default="Blog")
    sous_titre = models.TextField(default="Home > Blog")
    image_fond = models.ImageField(upload_to='blog/headers/', blank=True, null=True)

    def __str__(self):
        return f"Section Header du Blog"


class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Tag(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Article(models.Model):
    titre = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    image_card = models.ImageField(upload_to='blog/images_card/', help_text="Image affichée dans blog.html (liste)")
    image_detail = models.ImageField(upload_to='blog/images_detail/', help_text="Image principale de la page détail")
    image_banniere = models.ImageField(upload_to='blog/bannieres/',
                                       help_text="Image de bannière en haut de blog-single.html")

    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    intro = models.TextField(help_text="Paragraphe introductif")
    paragraphe_2 = models.TextField(blank=True, null=True)
    paragraphe_3 = models.TextField(blank=True, null=True)
    paragraphe_4 = models.TextField(blank=True, null=True)
    paragraphe_5 = models.TextField(blank=True, null=True)

    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='commentaires')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='reponses')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur} - {self.article}"