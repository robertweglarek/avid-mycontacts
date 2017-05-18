from django.contrib import admin

from .models import AddressBook, Entry


@admin.register(AddressBook)
class AddressBookAdmin(admin.ModelAdmin):
    pass


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'owner_username', 'email')

    def owner_username(self, obj):
        return obj.address_book.owner.username
    owner_username.short_description = 'Owner'
