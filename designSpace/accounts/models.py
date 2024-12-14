import logging

from cloudinary.api import delete_resources_by_prefix, delete_folder
from cloudinary.models import CloudinaryField
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from designSpace.accounts.managers import AppUserManager
from designSpace.accounts.utils import get_profile_image_folder
from designSpace.accounts.validators import validate_first_name, validate_last_name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True
    )

    username = models.CharField(
        unique=True,
        max_length=100,
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = AppUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email


logger = logging.getLogger('designSpace')


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    first_name = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        validators=[validate_first_name],
    )

    last_name = models.CharField(
        max_length=30,
        blank = True,
        null = True,
        validators=[validate_last_name],
    )

    profile_picture = CloudinaryField(
        'profile picture',
        folder=get_profile_image_folder,
        blank=True,
        null=True
    )

    profile_picture_public_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return None

    @property
    def display_name(self):
        return self.full_name or self.user.username

    def __str__(self):
        return self.full_name or "Anonymous"

    def delete(self, *args, **kwargs):

        folder_path = f"users/{self.user.username}/"
        delete_resources_by_prefix(folder_path)
        delete_folder(folder_path)

        self.user.delete()
        super().delete(*args, **kwargs)







