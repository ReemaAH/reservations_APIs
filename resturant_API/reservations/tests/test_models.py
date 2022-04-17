
import datetime

from model_bakery.recipe import Recipe
from reservations.models import Customer, Reservation, Table

from django.test import TestCase


class TableTestClass(TestCase):

    def setUp(self):
        self.table_recipe = Recipe(Table)

    def test_str(self):
        table = self.table_recipe.make()
        self.assertEqual(table.__str__(), "Table Number:" + str(table.number))


class ReservationTestClass(TestCase):

    def setUp(self):
       
        self.customer = Customer.objects.create(
            email="test@email.com",
            mobile_number="5000000005",
            full_name='test'
        )
        self.table = Table.objects.create(number="32", number_of_seats=2)
     
        self.reservation = Reservation.objects.create(
            date=datetime.datetime.now().date(),
            starting_time=datetime.time(10,00,00),
            ending_time=datetime.time(11,00,00),
            table=self.table,
            customer=self.customer)
        self.reservation.save()


    def test_str(self):
        self.assertEqual(
            self.reservation.__str__(), 
            self.reservation.customer.full_name + "-" + str(self.reservation.starting_time))


class CustomerTestClass(TestCase):

    def setUp(self):
       
        self.customer = Customer.objects.create(
            email="test@email.com",
            mobile_number="5000000005"
        )

    def test_str(self):
        self.assertEqual(
           self.customer.__str__(), self.customer.full_name)
