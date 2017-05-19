from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from utils.tests import BaseUserTestMixin
from .factories import AddressBookFactory, EntryFactory


class EntryUpdateTest(BaseUserTestMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.client.login(
            username=self.user_username,
            password=self.user_password,
        )

    def _make_url(self, pk):
        return reverse('contacts:entry-detail', args=[pk])

    def test_update_forbidden_for_guests(self):
        self.client.logout()
        address_book = AddressBookFactory(owner=self.user)
        entry = EntryFactory(address_book=address_book)
        url = self._make_url(entry.pk)

        response = self.client.put(url, {})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_others_entry(self):
        address_book = AddressBookFactory()
        entry = EntryFactory(address_book=address_book)
        url = self._make_url(entry.pk)

        response = self.client.put(url, {})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_own_entry_required_fields(self):
        address_book = AddressBookFactory(owner=self.user)
        entry = EntryFactory(address_book=address_book)
        url = self._make_url(entry.pk)
        required = ['first_name', 'last_name', 'mobile_number', 'address',
                    'email']

        response = self.client.put(url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        for field in required:
            self.assertIn(field, response.data.keys())

    def test_update_own_entry_email_validation(self):
        address_book = AddressBookFactory(owner=self.user)
        entry = EntryFactory(address_book=address_book)
        payload = {
            'first_name': entry.first_name,
            'last_name': entry.last_name,
            'mobile_number': entry.mobile_number,
            'address': entry.address,
            'email': 'ups!',
        }
        url = self._make_url(entry.pk)

        response = self.client.put(url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data.keys()), 1)
        self.assertIn('email', response.data.keys())

    def test_update_own_entry_valid_payload(self):
        address_book = AddressBookFactory(owner=self.user)
        entry = EntryFactory(address_book=address_book)
        payload = {
            'first_name': 'Robert',
            'last_name': 'Węglarek',
            'mobile_number': '11223344',
            'address': 'Far Away',
            'email': 'me@me.com',
        }
        url = self._make_url(entry.pk)

        response = self.client.put(url, payload)
        entry.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for name, value in payload.items():
            self.assertEqual(getattr(entry, name), value)
