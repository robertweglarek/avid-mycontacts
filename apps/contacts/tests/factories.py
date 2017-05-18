from django.contrib.auth import get_user_model
import factory

from apps.contacts.models import AddressBook, Entry

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """
    That would be usually placed somewhere else.
    """
    class Meta:
        model = User

    email = factory.Sequence(lambda n: 'test_user_{}@test.com'.format(n))
    username = factory.Sequence(lambda n: 'username{}'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'no-password')


class AddressBookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AddressBook

    owner = factory.SubFactory(UserFactory)


class EntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Entry

    address_book = factory.SubFactory(AddressBookFactory)
    first_name = factory.Sequence(lambda n: 'First{}'.format(n))
    last_name = factory.Sequence(lambda n: 'Last{}'.format(n))
    mobile_number = factory.Sequence(lambda n: '12345678{}'.format(n))
    address = factory.Sequence(lambda n: 'Address{}'.format(n))
    email = factory.Sequence(lambda n: 'email{}@test.com'.format(n))
