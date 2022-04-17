from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .managers import SoftDelete


class Table(SoftDelete):
    '''
    Table model

        - Fields
            1. number
            2. number_of_seats

    '''
    number = models.PositiveIntegerField(validators=[MinValueValidator(1)], unique=True)
    number_of_seats = models.PositiveIntegerField( validators=[MinValueValidator(1), MaxValueValidator(12)])
    
    def __str__(self):
        return "Table Number:" + str(self.number)


class Customer(SoftDelete):
    '''
   Customer model

        - Fields
            1. full_name
            2. email
            3. mobile_number

    '''

    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    mobile_number = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.full_name


class Reservation(SoftDelete):
    '''
    Reservation model

        - Fields
            1. date
            2. starting_time
            3. ending_time
            4. table
            5. customer
    '''

    date = models.DateField(blank=True, null=True)
    starting_time = models.TimeField(blank=True, null=True)
    ending_time = models.TimeField(blank=True, null=True)
    table = models.ForeignKey(Table,
                              on_delete=models.CASCADE,
                              related_name='+',
                              verbose_name=('table'))
    customer = models.ForeignKey(Customer,
                                          on_delete=models.CASCADE,
                                          related_name='+',
                                          verbose_name=('customer'))
    def __str__(self):
        return self.customer.full_name + "-" + str(self.starting_time)
