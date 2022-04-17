from rest_framework import serializers

from .models import Customer, Reservation, Table


class TableSerializer(serializers.ModelSerializer):
   class Meta:
       model = Table
       fields = ('number', 'number_of_seats')


class CustomerSerializer(serializers.ModelSerializer):
   class Meta:
       model = Customer
       fields = ('email', 'mobile_number')


class ReservationSerializer(serializers.Serializer):
    date = serializers.DateField()
    starting_time = serializers.TimeField()
    ending_time = serializers.TimeField()
    customer = CustomerSerializer()
    table = TableSerializer()


class CreateReservationSerializer(serializers.Serializer):
    
    date = serializers.DateField(required=True)
    starting_time = serializers.TimeField(required=True)
    ending_time = serializers.TimeField(required=True)
    customer_email = serializers.EmailField(required=True)
    customer_mobile = serializers.CharField(required=True)
    table_number = serializers.IntegerField(required=True)

    def create(self, validated_data):
        """
        Create and return a new  reservation instance, given the validated data.
        """
        customer = Customer.objects.create(
            email=validated_data['customer_email'],
            mobile_number=validated_data['customer_mobile']
        )
        customer.save()
        table = Table.objects.get(number=validated_data['table_number'])
        reservation = Reservation.objects.create(
            date=validated_data['date'],
            starting_time=validated_data['starting_time'],
            ending_time=validated_data['ending_time'],
            table=table,
            customer=customer
        )
        reservation.save()
        return reservation
