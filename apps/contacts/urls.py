from rest_framework import routers

from .views import AddressBookViewSet, EntryViewSet

router = routers.DefaultRouter()
router.register(r'address-book', AddressBookViewSet, base_name='address-book')
router.register(r'entry', EntryViewSet, base_name='entry')

urlpatterns = router.urls
