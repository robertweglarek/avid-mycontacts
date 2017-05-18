from django.conf import settings
from django.db import models


class AddressBook(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.owner.username


class Entry(models.Model):
    address_book = models.ForeignKey(AddressBook)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField()

    class Meta:
        verbose_name_plural = 'Entries'

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
