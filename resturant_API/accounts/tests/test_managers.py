from accounts.models import CustomUser

from django.contrib.auth.models import Group, Permission
from django.test import TestCase


class UserManagerTestClass(TestCase):

    def setUp(self):
        # Setup run before every test method.
        self.create_Admins_group()

        # create admin group
    def create_Admins_group(self):
        permissions = ['add_table', 'change_table', 'delete_table',
                   'view_table', 'add_customuser', "view_customuser"]

        admins_group = Group.objects.create(name='Admins')
        for p in permissions:
            permission = Permission.objects.get(codename=p)
            admins_group.permissions.add(permission)

    def test_admin_role(self):
        user = CustomUser.objects._create_user(
            employee_number="2349", 
            role=1, 
            password="Rsdfv@2234", 
            first_name= "test", last_name="test"
        )
        self.assertEqual(user.groups.filter(name='Admins').exists(), True)

    def test_employee_role(self):
        # if user's role is 2, then s/he will not be added to admins group
        user = CustomUser.objects._create_user(
            employee_number="2349", 
            role=2, 
            password="Rsdfv@2234", 
            first_name= "test", last_name="test"
        )
        self.assertEqual(user.groups.filter(name='Admins').exists(), False)
    
    def test_super_user_default_values(self):
        super_user = CustomUser.objects.create_superuser(
            employee_number="2349", 
            password="Rsdfv@2234", 
            first_name= "test", last_name="test"
        )
        self.assertEqual(super_user.is_staff, True)
        self.assertEqual(super_user.is_superuser, True)
        self.assertEqual(super_user.role, 1)
        self.assertEqual(super_user.groups.filter(name='Admins').exists(), True)

    def test_super_user_not_is_staff(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
            employee_number="2349", 
            password="Rsdfv@2234", 
            is_staff = False,
            first_name= "test", last_name="test")

            created = False
            self.assertEqual(created, False)
    
    def test_super_user_not_is_superuser(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
            employee_number="2349", 
            password="Rsdfv@2234", 
            is_superuser= False,
            first_name= "test", last_name="test")

            created = False
            self.assertEqual(created, False)
    
    def test_super_user_role(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
            employee_number="2349", 
            password="Rsdfv@2234", 
            role=2,
            first_name= "test", last_name="test")

            created = False
            self.assertEqual(created, False)
