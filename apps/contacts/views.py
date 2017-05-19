from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from .models import Entry
from .serializers import AddressBookSerializer, EntrySerializer


class AddressBookViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddressBookSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EntryViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('first_name', 'last_name', 'mobile_number', 'address',
                     'email')
    permission_classes = (IsAuthenticated,)
    serializer_class = EntrySerializer

    def get_queryset(self):
        return Entry.objects.filter(address_book__owner=self.request.user)
