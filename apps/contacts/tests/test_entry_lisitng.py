from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from utils.tests import BaseUserTestMixin
from .factories import AddressBookFactory, EntryFactory


class EntryListingTest(BaseUserTestMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('contacts:entry-list')
        self.client.login(
            username=self.user_username,
            password=self.user_password,
        )

    def test_listing_forbidden_for_guests(self):
        self.client.logout()

        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_listing_only_owned_entries_listed(self):
        address_book = AddressBookFactory(owner=self.user)
        owned_entry = EntryFactory(address_book=address_book)
        EntryFactory()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], owned_entry.id)
