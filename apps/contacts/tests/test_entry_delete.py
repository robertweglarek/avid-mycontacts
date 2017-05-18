from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.contacts.models import Entry
from utils.tests import BaseUserTestMixin
from .factories import AddressBookFactory, EntryFactory


class EntryDeleteTest(BaseUserTestMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.client.login(
            username=self.user_username,
            password=self.user_password,
        )

    def _make_url(self, pk):
        return reverse('contacts:entry-detail', args=[pk])

    def test_delete_forbidden_for_guests(self):
        self.client.logout()
        address_book = AddressBookFactory(owner=self.user)
        entry = EntryFactory(address_book=address_book)
        url = self._make_url(entry.pk)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_others_entry(self):
        address_book = AddressBookFactory()
        entry = EntryFactory(address_book=address_book)
        url = self._make_url(entry.pk)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_own_entry(self):
        address_book = AddressBookFactory(owner=self.user)
        entry = EntryFactory(address_book=address_book)
        url = self._make_url(entry.pk)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Entry.objects.filter(id=entry.id).exists())
