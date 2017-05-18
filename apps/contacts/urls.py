from rest_framework import routers

from .views import AddressBookViewSet

router = routers.DefaultRouter()
router.register(r'address-book', AddressBookViewSet, base_name='address-book')

urlpatterns = router.urls
