from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.contacts.models import Entry
from utils.tests import BaseUserTestMixin
from .factories import AddressBookFactory, EntryFactory


class EntryListTest(BaseUserTestMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('contacts:entry-list')
        self.client.login(
            username=self.user_username,
            password=self.user_password,
        )

    def test_list_forbidden_for_guests(self):
        self.client.logout()

        response = self.client.get(self.url, {})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_only_owned_entries_listed(self):
        address_book = AddressBookFactory(owner=self.user)
        owned_entry = EntryFactory(address_book=address_book)
        EntryFactory()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], owned_entry.id)

    def test_list_without_address_book(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_with_filtering(self):
        address_book = AddressBookFactory(owner=self.user)
        EntryFactory.create_batch(5, address_book=address_book)
        filters_schema = {
            'first_name': 'TestFirstName', 'last_name': 'TestLastName',
            'mobile_number': 1234512340, 'address': 'Hello World!',
            'email': 'uniquetest@email.com'
        }
        entry = EntryFactory(
            address_book=address_book,
            first_name=filters_schema['first_name'],
            last_name=filters_schema['last_name'],
            mobile_number=filters_schema['mobile_number'],
            address=filters_schema['address'],
            email=filters_schema['email'],
        )
        url = self._get_url_with_filters(filters_schema)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], entry.id)

    def _get_url_with_filters(self, filters_schema):
        filters = ['{}={}'.format(k, v) for k, v in filters_schema.items()]
        filters_query = '&'.join(filters)
        url = '{}?{}'.format(self.url, filters_query)
        return url
