from django.core import validators
from django.db import models
from django.contrib.auth import models as auth_models
from cloudinary import models as cloudinary_models


class CustomUserManager(auth_models.BaseUserManager):
    """
    The email is the unique identifiers for authentication instead of usernames.
    """

    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
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

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUser(auth_models.AbstractUser):
    MAX_LEN_NAME = 30
    MIN_LEN_NAME = 2

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    object = CustomUserManager()

    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=MAX_LEN_NAME,
        validators=(
            validators.MinLengthValidator(MIN_LEN_NAME),
        ),
        blank=True,
        null=True,
    )
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

    def __str__(self):
        return str(self.email)
