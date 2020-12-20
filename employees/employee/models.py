from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


# Create your models here.


class UserProfileManager(BaseUserManager):
    """ Helps django to work with our custom user model"""

    def create_new(self, email, name, password=None):
        """" Create a new user profile object  """

        if not email:
            raise ValueError('User must have an email address')

        # normalize the email address by lower casing domain part of it, validate if email is in the standard format.
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        # set_password encrypt our password
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """" Create a new super user with given details """

        user = self.create_new(email, name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ User profile model"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """ Used to get full name of user """

        return self.name

    def get_short_name(self):
        """ Used to get short name of user """

        return self.name

    def __str__(self):
        """ Used to convert django object into a string """

        return self.name

    """ 
    This code will help us to return all tasks associated with this user even if we do not have it in user model
    By property keyword and then return self, with model name in small letter e.i self.tasks.all()
    Then call this property function in serializer where we call User serializer 
    """
    @property
    def tasks(self):
        return self.tasks_set.all()


class Tasks(models.Model):
    """ Profile feeds """

    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=300)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.name
