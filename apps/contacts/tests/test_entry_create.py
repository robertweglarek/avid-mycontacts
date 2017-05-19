from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.contacts.models import Entry
from utils.tests import BaseUserTestMixin
from .factories import AddressBookFactory


class EntryCreateTest(BaseUserTestMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.client.login(
            username=self.user_username,
            password=self.user_password,
        )
        self._payload = {
            'first_name': 'Robert',
            'last_name': 'Węglarek',
            'mobile_number': '11223344',
            'address': 'Far Away',
            'email': 'me@me.com',
        }

    def _make_url(self):
        return reverse('contacts:entry-list')

    def test_create_forbidden_for_guests(self):
        self.client.logout()
        url = self._make_url()

        response = self.client.post(url, self._payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_without_address_book(self):
        url = self._make_url()

        response = self.client.post(url, self._payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_required_fields(self):
        AddressBookFactory(owner=self.user)
        url = self._make_url()
        required = ['first_name', 'last_name', 'mobile_number', 'address',
                    'email']

        response = self.client.post(url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        for field in required:
            self.assertIn(field, response.data.keys())

    def test_create_email_validation(self):
        AddressBookFactory(owner=self.user)
        url = self._make_url()
        self._payload['email'] = 'invalid!'

        response = self.client.post(url, self._payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data.keys()), 1)
        self.assertIn('email', response.data.keys())

    def test_create_valid_payload(self):
        address_book = AddressBookFactory(owner=self.user)
        url = self._make_url()

        response = self.client.post(url, self._payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        entry = Entry.objects.first()
        self.assertEqual(entry.address_book, address_book)
        for name, value in self._payload.items():
            self.assertEqual(getattr(entry, name), value)
