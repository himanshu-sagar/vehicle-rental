from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):

    fieldsets = (
        (None, {
            'fields': ('phone', 'username')
        }),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
            )
        }),
        # (_('Permissions'), {
        #     'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        # }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )

    list_display = ['id', 'phone', 'first_name', 'last_name', 'is_staff', 'username', 'is_customer', 'is_store_manager']
    search_fields = ('id', 'phone', 'first_name', 'last_name', "username", 'is_customer', 'is_store_manager')


admin.site.register(User, UserAdmin)