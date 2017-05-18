from django.contrib.auth import get_user_model
import factory

from apps.contacts.models import AddressBook

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
