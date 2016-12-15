from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from stdimage.models import StdImageField


class AccountUserManager(UserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):

        now = timezone.now()
        if not email:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        user = self.model(username=email,
                          email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractUser):
    objects = AccountUserManager()
    stripe_id = models.CharField(max_length=40, default='')
    subscription_end = models.DateTimeField(default=timezone.now)
    public_name = models.CharField(max_length=20)
    location = models.CharField(max_length=20, blank=True, null=True)
    profile_image = StdImageField(upload_to="images/user_profiles",
                                  variations={
                                      'small': {'width': 96, 'height': 96, "crop": True}
                                  },
                                  blank=True, null=True)

