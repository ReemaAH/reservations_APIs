import datetime

from accounts.models import CustomUser
from reservations.models import Customer, Reservation, Table
from rest_framework.test import APIClient

from django.contrib.auth.models import Group, Permission
from django.test import TestCase


class TableApiListTestClass(TestCase):
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

    def test_create_table(self):
        payload = {
            'table_number': "1", 
            'number_of_seats': 2, 
        }

        response = self.client.post('/api/reservations/tables', payload)
        is_table= Table.objects.filter(number="1").exists()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(is_table, True)


    def test_create_table_with_same_number(self):
        Table.objects.create(number="2", number_of_seats=2)
        payload = {
            'table_number': "2", 
            'number_of_seats': 2, 
        }
        response = self.client.post('/api/reservations/tables', payload)
        is_table= Table.objects.filter(number="2").exists()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(is_table, True)


    def test_get_tables(self):
        response = self.client.get('/api/reservations/tables')
        self.assertEqual(response.status_code, 200)

class TableApiDetailTestClass(TestCase):
    def setUp(self):
  
        self.create_Admins_group()

        # create a user with admin role
        self.user = CustomUser.objects._create_user(
            employee_number="2341", 
            role=1, 
            password="Rsdfv@2234", 
            first_name= "test", last_name="test"
        )
        # setup client
        self.client = APIClient()
        # login with that user
        self.access_token = self.client.post('/api/auth/login',{
        "employee_number" : "2341" ,
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
    
    def test_get_table(self):
        Table.objects.create(number="55", number_of_seats=2)
        response = self.client.get('/api/reservations/tables/55/')
        self.assertEqual(response.status_code, 200)

    def test_get_table_None(self):
        response = self.client.get('/api/reservations/tables/51/')
        self.assertEqual(response.status_code, 400)
    
    def test_update_table(self):
        Table.objects.create(number="40", number_of_seats=2)
        payload = {
            'number_of_seats': 2, 
        }
        response = self.client.put('/api/reservations/tables/40/', payload)
        self.assertEqual(response.status_code, 200)
 
    def test_update_table_None(self):
        payload = {
            'number_of_seats': 2, 
        }
        response = self.client.put('/api/reservations/tables/89/', payload)
        self.assertEqual(response.status_code, 400)

    def test_update_table_invalid_type(self):
        Table.objects.create(number="98", number_of_seats=2)
        payload = {
            'number_of_seats': "test", 
        }
        response = self.client.put('/api/reservations/tables/98/', payload)
        self.assertEqual(response.status_code, 400)
    
    def test_delete_table(self):
        Table.objects.create(number="32", number_of_seats=2)
      
        response = self.client.delete('/api/reservations/tables/32/')
        self.assertEqual(response.status_code, 200)
    
    def test_delete_table_None(self):
        response = self.client.delete('/api/reservations/tables/64/')
        self.assertEqual(response.status_code, 400)
    
class ReservationApiListViewTestClass(TestCase):

    def setUp(self):
  
        self.create_Admins_group()

        # create a user with admin role
        self.user = CustomUser.objects._create_user(
            employee_number="2341", 
            role=1, 
            password="Rsdfv@2234", 
            first_name= "test", last_name="test"
        )
        # setup client
        self.client = APIClient()
        # login with that user
        self.access_token = self.client.post('/api/auth/login',{
        "employee_number" : "2341" ,
        "password" : "Rsdfv@2234"}).data['access']
    
        # add token to client header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.customer = Customer.objects.create(
            email="test@email.com",
            mobile_number="5000000005"
        )
        self.table = Table.objects.create(number="32", number_of_seats=2)
     
        self.reservation = Reservation.objects.create(
            date=datetime.datetime.now().date(),
            starting_time=datetime.time(10,00,00),
            ending_time=datetime.time(11,00,00),
            table=self.table,
            customer=self.customer
        )

    def create_Admins_group(self):
        permissions = [
            'add_table', 'change_table', 'delete_table',
            'view_table', 'add_customuser', "view_customuser"]

        admins_group = Group.objects.create(name='Admins')
        for p in permissions:
            permission = Permission.objects.get(codename=p)
            admins_group.permissions.add(permission)

    def test_get_reservations_ascending(self):
        self.reservation = Reservation.objects.create(
            date=datetime.datetime.now().date(),
            starting_time=datetime.time(10,00,00),
            ending_time=datetime.time(11,00,00),
            table=self.table,
            customer=self.customer
        )

        response = self.client.get('/api/reservations/?page=1&sort=1')
        self.assertEqual(response.status_code, 200)

    def test_get_reservations_descending(self):
        self.reservation = Reservation.objects.create(
            date=datetime.datetime.now().date(),
            starting_time=datetime.time(13,00,00),
            ending_time=datetime.time(14,00,00),
            table=self.table,
            customer=self.customer
        )

        response = self.client.get('/api/reservations/?page=1&sort=-1')
        self.assertEqual(response.status_code, 200)
    
    def test_create_valid_reservation(self):
        payload = {
            "date": "2022-04-17",
            "starting_time": "18:00", 
            "ending_time": "19:00",
            "customer_email": "test@email.com",
            "customer_mobile": "580324908",
            "table_number": 32
        }
        response = self.client.post('/api/reservations/', payload)
        self.assertEqual(response.status_code, 201)
    
    def test_create_invalid_reservation(self):
        payload = {
            "starting_time": "18:00", 
            "ending_time": "19:00",
            "customer_email": "test@email.com",
            "customer_mobile": "580324908",
            "table_number": 32
        }
        response = self.client.post('/api/reservations/', payload)
        self.assertEqual(response.status_code, 400)

    def test_create_reservation_not_within_working_hours(self):
        payload = {
            "date": "2022-04-17",
            "starting_time": "9:00", 
            "ending_time": "10:00",
            "customer_email": "test@email.com",
            "customer_mobile": "580324908",
            "table_number": 32
        }
        response = self.client.post('/api/reservations/', payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['result'], 
            'reservation should be with the working hours: 12:00:00 - 23:59:00')

    
    def test_create_reservation_overlapping(self):
        payload = {
            "date": "2022-04-17",
            "starting_time": "15:00", 
            "ending_time": "16:00",
            "customer_email": "test@email.com",
            "customer_mobile": "580324908",
            "table_number": 32
        }
        payload1 = {
            "date": "2022-04-17",
            "starting_time": "15:30", 
            "ending_time": "16:00",
            "customer_email": "test1@email.com",
            "customer_mobile": "581324908",
            "table_number": 32
        }
        self.client.post('/api/reservations/', payload)
        response = self.client.post('/api/reservations/', payload1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['result'], 
            'Sorry, this time slot is reserved, please pick a new time slot')
    
    def test_delete_reservation(self):
        payload = {
            "date": str(datetime.datetime.now().date()),
            "starting_time": "17:00", 
            "ending_time": "18:00",
            "customer_email": "test@email.com",
            "customer_mobile": "580324908",
            "table_number": 32
        }
        self.client.post('/api/reservations/', payload)
        response = self.client.delete('/api/reservations/17/')
        self.assertEqual(response.status_code, 200)
    
    def test_delete_reservation_None(self):
        response = self.client.delete('/api/reservations/15/')
        self.assertEqual(response.status_code, 400)


class AvailableReservationsTimeSlotsViewTestClass(TestCase):

    def setUp(self):
  
        self.create_Admins_group()

        # create a user with admin role
        self.user = CustomUser.objects._create_user(
            employee_number="2341", 
            role=1, 
            password="Rsdfv@2234", 
            first_name= "test", last_name="test"
        )
        # setup client
        self.client = APIClient()
        # login with that user
        self.access_token = self.client.post('/api/auth/login',{
        "employee_number" : "2341" ,
        "password" : "Rsdfv@2234"}).data['access']
    
        # add token to client header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.customer = Customer.objects.create(
            email="test@email.com",
            mobile_number="5000000005"
        )
        self.table = Table.objects.create(number="32", number_of_seats=2)

    def create_Admins_group(self):
        permissions = [
            'add_table', 'change_table', 'delete_table',
            'view_table', 'add_customuser', "view_customuser"]

        admins_group = Group.objects.create(name='Admins')
        for p in permissions:
            permission = Permission.objects.get(codename=p)
            admins_group.permissions.add(permission)
    
    def test_check_available_time_slots_1(self):
        payload = {
            "date": str(datetime.datetime.now().date()),
            "starting_time": "17:00", 
            "ending_time": "18:00",
            "customer_email": "test@email.com",
            "customer_mobile": "580324908",
            "table_number": 32
        }
        self.client.post('/api/reservations/', payload)
        response = self.client.get('/api/reservations/time-slots/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['32'], ['12:00:00 - 17:00:00', '18:00:00 - 23:59:00'])

    def test_check_available_time_slots_2(self):
        payload = {
            "date": str(datetime.datetime.now().date()),
            "starting_time": "17:00", 
            "ending_time": "18:00",
            "customer_email": "test@email.com",
            "customer_mobile": "580324908",
            "table_number": 32
        }
        payload1 = {
            "date": str(datetime.datetime.now().date()),
            "starting_time": "19:00", 
            "ending_time": "20:10",
            "customer_email": "test@email.com",
            "customer_mobile": "580324908",
            "table_number": 32
        }
        self.client.post('/api/reservations/', payload)
        self.client.post('/api/reservations/', payload1)
        response = self.client.get('/api/reservations/time-slots/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['32'], 
        ['12:00:00 - 17:00:00', '18:00:00 - 19:00:00', '20:10:00 - 23:59:00'])
    
    def test_check_available_time_slots_with_no_previous_reservation(self):

        response = self.client.get('/api/reservations/time-slots/1/')
        self.assertEqual(response.status_code, 200)
      

class ReservationsByFiltersListViewTestClass(TestCase):
    def setUp(self):
  
        self.create_Admins_group()

        # create a user with admin role
        self.user = CustomUser.objects._create_user(
            employee_number="2341", 
            role=1, 
            password="Rsdfv@2234", 
            first_name= "test", last_name="test"
        )
        # setup client
        self.client = APIClient()
        # login with that user
        self.access_token = self.client.post('/api/auth/login',{
        "employee_number" : "2341" ,
        "password" : "Rsdfv@2234"}).data['access']
    
        # add token to client header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.customer = Customer.objects.create(
            email="test@email.com",
            mobile_number="5000000005"
        )
        self.table = Table.objects.create(number="32", number_of_seats=2)
        self.table1 = Table.objects.create(number="80", number_of_seats=2)
        self.table1 = Table.objects.create(number="90", number_of_seats=2)

    def create_Admins_group(self):
        permissions = [
            'add_table', 'change_table', 'delete_table',
            'view_table', 'add_customuser', "view_customuser"]

        admins_group = Group.objects.create(name='Admins')
        for p in permissions:
            permission = Permission.objects.get(codename=p)
            admins_group.permissions.add(permission)
    
    def test_get_queryset_with_no_filters(self):
        payload = {
            "date": str(datetime.datetime.now().date()),
            "starting_time": "19:00", 
            "ending_time": "20:10",
            "customer_email": "test@email.com",
            "customer_mobile": "580324908",
            "table_number": 32
        }
        self.client.post('/api/reservations/', payload)
        response = self.client.get('/api/reservations/all/')
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.status_code, 200)
    
    def test_get_queryset_with_tables_filter(self):
        payload = {
            "date": str(datetime.datetime.now().date()),
            "starting_time": "13:00", 
            "ending_time": "13:00",
            "customer_email": "test@email.com",
            "customer_mobile": "580324908",
            "table_number": 32
        }
        payload1 = {
            "date": str(datetime.datetime.now().date()),
            "starting_time": "15:00", 
            "ending_time": "18:10",
            "customer_email": "test@email.com",
            "customer_mobile": "580777908",
            "table_number": 80
        }
        payload2 = {
            "date": str(datetime.datetime.now().date()),
            "starting_time": "20:00", 
            "ending_time": "22:00",
            "customer_email": "test@email.com",
            "customer_mobile": "580777908",
            "table_number": 90
        }
        self.client.post('/api/reservations/', payload)
        self.client.post('/api/reservations/', payload1)
        self.client.post('/api/reservations/', payload2)
        response = self.client.get('/api/reservations/all/?tables=32,90')
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.status_code, 200)


    def test_get_queryset_with_starting_date_filter(self):
        payload = {
            "date": str(datetime.datetime.now().date()),
            "starting_time": "19:00", 
            "ending_time": "20:10",
            "customer_email": "test@email.com",
            "customer_mobile": "580324908",
            "table_number": 32
        }
        payload1 = {
            "date": str(datetime.datetime(2020, 5, 17).date()),
            "starting_time": "20:00", 
            "ending_time": "22:00",
            "customer_email": "test@email.com",
            "customer_mobile": "580777908",
            "table_number": 90
        }
        self.client.post('/api/reservations/', payload)
        self.client.post('/api/reservations/', payload1)
        response = self.client.get('/api/reservations/all/?starting_date='+str(datetime.datetime.now().date()))
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.status_code, 200)
    
    def test_get_queryset_with_ending_date_filter(self):
        payload = {
            "date": str(datetime.datetime.now().date()),
            "starting_time": "19:00", 
            "ending_time": "20:10",
            "customer_email": "test@email.com",
            "customer_mobile": "580324908",
            "table_number": 32
        }
        payload1 = {
            "date": str(datetime.datetime(2020, 5, 17).date()),
            "starting_time": "20:00", 
            "ending_time": "22:00",
            "customer_email": "test@email.com",
            "customer_mobile": "580777908",
            "table_number": 90
        }
        self.client.post('/api/reservations/', payload)
        self.client.post('/api/reservations/', payload1)
        response = self.client.get('/api/reservations/all/?ending_date='+str(datetime.datetime.now().date()))
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.status_code, 200)
