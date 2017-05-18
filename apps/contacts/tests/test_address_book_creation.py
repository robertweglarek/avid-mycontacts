from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.contacts.models import AddressBook
from utils.tests import BaseUserTestMixin
from .factories import AddressBookFactory


class AddressBookCreationTest(BaseUserTestMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('contacts:address-book-list')
        self.client.login(
            username=self.user_username,
            password=self.user_password,
        )

    def test_creation_forbidden_for_guests(self):
        self.client.logout()

        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_creation_when_does_not_exist(self):
        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            AddressBook.objects.filter(owner=self.user).count(), 1)

    def test_creation_when_already_exists(self):
        AddressBookFactory(owner=self.user)
        self.client.post(self.url, {})

        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            AddressBook.objects.filter(owner=self.user).count(), 1)

    def test_creation_when_not_owned_exist(self):
        AddressBookFactory()

        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            AddressBook.objects.filter(owner=self.user).count(), 1)
