from django.contrib.auth.hashers import make_password
from django.core import validators
from django.db import models
from django.contrib.auth import models as auth_models
from cloudinary import models as cloudinary_models


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
    MAX_LEN_NAME = 100
    MIN_LEN_NAME = 2

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    object = CustomUserManager()

    email = models.EmailField(unique=True)
    first_name = models.CharField(
        max_length=MAX_LEN_NAME,
        validators=(
            validators.MinLengthValidator(MIN_LEN_NAME),
        ),
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=MAX_LEN_NAME,
        validators=(
            validators.MinLengthValidator(MIN_LEN_NAME),
        ),
        blank=True,
        null=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    profile_picture = cloudinary_models.CloudinaryField(
        null=True,
        blank=True,
    )
    is_sandboxed = models.BooleanField(default=True)
    is_valid = models.BooleanField(default=False)
