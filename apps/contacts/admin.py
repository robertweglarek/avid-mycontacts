from django.contrib import admin

from .models import AddressBook


@admin.register(AddressBook)
class AddressBookAdmin(admin.ModelAdmin):
    pass
