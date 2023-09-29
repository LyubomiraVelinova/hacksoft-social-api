from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth import models as auth_models


class CustomUserManager(auth_models.BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError("The email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class CustomUser(auth_models.AbstractUser):
    MAX_LEN_NAME = 200

    USERNAME_FIELD = "email"
    object = CustomUserManager()

    email = models.EmailField(unique=True)
    name = models.CharField(
        max_length=MAX_LEN_NAME,
        blank=True,
        null=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
    )
    is_sandboxed = models.BooleanField(default=True)
