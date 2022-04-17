from webbrowser import get
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Dump Objects to Database'

    def handle(self, *args, **kwargs):
        print('dumping db')
        self.create_Admins_group()
        self.create_superuser()

    def create_Admins_group(self):
        print('create admins group')
        permissions = ['add_table', 'change_table', 'delete_table',
                   'view_table', 'add_customuser', "view_customuser"]

        try:
            Group.objects.get(name='Admins')
        except Group.DoesNotExist:
            admins_group = Group.objects.create(name='Admins')
            for p in permissions:
                permission = Permission.objects.get(codename=p)
                admins_group.permissions.add(permission)


    def create_superuser(self):
        print('create superuser')
        try:
            CustomUser.objects.get(employee_number="1111")
        except CustomUser.DoesNotExist:
            CustomUser.objects.create_superuser(
                employee_number="1111",
                password="ser$56GGxz21",
                first_name="Admin",
                last_name="Admin",
                role=1
            )
            

