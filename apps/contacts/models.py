from django.conf import settings
from django.db import models


class AddressBook(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)
