from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('employee_number', 'is_staff', 'is_active',)
    list_filter = ('employee_number', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('employee_number', 'role', 'first_name', 'last_name')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('employee_number', 'password1', 'password2', 'role', 'first_name', 'last_name')}
        ),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions',)}),
    )

    search_fields = ('employee_number',)
    ordering = ('employee_number',)


admin.site.register(CustomUser, CustomUserAdmin)
