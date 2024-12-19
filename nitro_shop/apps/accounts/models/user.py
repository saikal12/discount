from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    # Basic Information
    email = models.EmailField(("email address"), unique=True)
    is_email_verified = models.BooleanField(default=False, verbose_name=("email verified"))
    username = models.CharField(("username"), max_length=150, blank=True, null=True)
    role = models.ForeignKey("Role", on_delete=models.SET_NULL, null=True)
    is_staff = models.BooleanField(
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text=("Designates that this user has all permissions without explicitly assigning them."),
    )

    # Object Manager
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def has_role(self, role_name):
        return self.roles.filter(name=role_name).exists()