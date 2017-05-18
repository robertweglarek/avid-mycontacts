from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from .serializers import AddressBookSerializer


class AddressBookViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddressBookSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
