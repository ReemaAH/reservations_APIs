from accounts.models import CustomUser
from rest_framework.test import APIClient

from django.contrib.auth.models import Group, Permission
from django.test import TestCase


class EmployeeRegistrationTestClass(TestCase):
    def setUp(self):
  
        self.create_Admins_group()

        # create a user with admin role
        CustomUser.objects._create_user(
            employee_number="2349", 
            role=1, 
            password="Rsdfv@2234", 
            first_name= "test", last_name="test"
        )
        # setup client
        self.client = APIClient()
        # login with that user
        self.access_token = self.client.post('/api/auth/login',{
        "employee_number" : "2349" ,
        "password" : "Rsdfv@2234"}).data['access']

        # add token to client header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')


    def create_Admins_group(self):
        permissions = [
            'add_table', 'change_table', 'delete_table',
            'view_table', 'add_customuser', "view_customuser"]

        admins_group = Group.objects.create(name='Admins')
        for p in permissions:
            permission = Permission.objects.get(codename=p)
            admins_group.permissions.add(permission)


    def test_create_employee(self):
        payload = {"employee_number": "1196",
                "role": 1,
                "password": "Rsdfv@2234",
                "first_name": "test",
                "last_name": "test"}
    
        self.client.post('/api/employee/registration', payload)

        is_user = CustomUser.objects.filter(employee_number="1196").exists()
        self.assertEqual(is_user, True)


    def test_create_employee_with_the_same_number(self):
        CustomUser.objects._create_user(
            employee_number="1111", 
            role=1, 
            password="Rsdfv@2234", 
            first_name= "test", last_name="test"
        )
        payload = {"employee_number": "1111",
                "role": "1",
                "password": "Rsdfv@2234",
                "first_name": "test",
                "last_name": "test"}
    
        response = self.client.post('/api/employee/registration', payload)
        self.assertEqual(response.status_code, 400)


    def test_create_employee_with_missing_feild(self):
        payload = {
                "role": "1",
                "password": "Rsdfv@2234",
                "first_name": "test",
                "last_name": "test"}
    
        response = self.client.post('/api/employee/registration', payload)
        self.assertEqual(response.status_code, 400)
