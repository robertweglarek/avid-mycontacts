from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from .models import AddressBook, Entry


class AddressBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressBook
        fields = ('id',)

    def validate(self, data):
        self._ensure_no_addressbook()
        return data

    def _ensure_no_addressbook(self):
        user = self.context['request'].user
        addressbook_exists = AddressBook.objects.filter(owner=user).exists()
        if addressbook_exists:
            raise ValidationError('Address book has been alredy created')


class EntrySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Entry
        fields = ('id', 'first_name', 'last_name', 'mobile_number', 'address',
                  'email')
