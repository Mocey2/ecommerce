# authentification/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, prenom, nom, password=None, role='vendeur'):
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, prenom=prenom, nom=nom, role=role)
        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, prenom, nom, password):
        user = self.create_user(email, prenom, nom, password, role='admin')
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user

ROLE_CHOICES = (
    ('vendeur', 'Vendeur'),
    ('admin', 'Admin'),
)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='vendeur')
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['prenom', 'nom']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def save(self, *args, **kwargs):
        if self.is_admin:
            self.role = 'admin'
        if not self.role:
            self.role = 'vendeur'
        super().save(*args, **kwargs)

    @property
    def is_staff(self):
        return self.is_admin
