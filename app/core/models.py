import os
import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin


def singer_image_file_path(instance, filename):
    """Generate file path for singer image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/singer/', filename)


class UserManager(BaseUserManager):
    """User manager class"""

    def create_user(self, email, password=None, **extra_fields):
        """Create user based on email and password

        Parameters
        ----------
        email : str
            user's email address
        password : str
            user's password

        Returns
        -------
        User
            the user just created
        """
        if not email or not password:
            raise ValueError({'error': 'Email and password re required.'})
        # create a new user model
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # set password
        user.set_password(password)
        # save the model
        user.save(using=self.db)

        # return the user just created
        return user

    def create_superuser(self, email, password=None):
        """Create a new superuser

        Parameters
        ----------
        email : str
            user's email address
        password : str
            user's password

        Returns
        -------
        User
            the user just created
        """
        # create a user using create_user method
        user = self.create_user(email, password)
        # set user as superuser and staff
        user.is_superuser = True
        user.is_staff = True
        # save the model
        user.save(using=self.db)

        # return the user just created
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        """Display string type of user """
        return self.email


class Singer(models.Model):
    """Singer model"""
    name = models.CharField(max_length=255, blank=False)
    image = models.ImageField(null=True, upload_to=singer_image_file_path)

    def __str__(self):
        return self.name


class Song(models.Model):
    """Song model"""
    title = models.CharField(max_length=255, blank=False)
    length = models.DecimalField(max_digits=4, decimal_places=2)
    release = models.DateTimeField()
    singers = models.ManyToManyField('Singer')

    def __str__(self) -> str:
        return self.title


class PlayList(models.Model):
    """User's play list"""
    name = models.CharField(max_length=255, blank=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    songs = models.ManyToManyField('Song', blank=True)

    def __str__(self):
        return self.name
