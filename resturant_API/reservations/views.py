import datetime
import json

from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from django.contrib.auth.mixins import AccessMixin
from django.core.cache import cache
from django.db.models import Q

from .models import Reservation, Table
from .serializers import (
    CreateReservationSerializer, ReservationSerializer, TableSerializer,
)

CACHE_TTL = settings.CACHE_TTL
starting_woring_time = datetime.time(12,00,00)
ending_working_time = datetime.time(23,59,00)
print("starting_woring_time: " + str(starting_woring_time ))
print("ending_working_time: " + str(ending_working_time) )
max_number_of_seats = 12


class AdminRoleMixin(AccessMixin):
    '''
    AdminRoleMixin
    Checks if the user is in the admin group.
    '''

    def dispatch(self, request, *args, **kwargs):
        req = self.initialize_request(request, *args, **kwargs)
        if not req.user.is_authenticated:
            return self.handle_no_permission()
        if req.user.id in cache:
            # using cached data
            is_admin = cache.get(req.user.id)
        else:
            # store data in cache
            group = ("Admins" if self.request.user.groups.filter(name='Admins').exists() else "")
            cache.set(req.user.id, group, timeout=CACHE_TTL)
            is_admin = cache.get(req.user.id)
        
        if not is_admin:
            return Response(
                {"result": "You're not authorized"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().dispatch(request, *args, **kwargs)


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 5


class TableApiListView(AdminRoleMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        List all the tables
        '''
        tables = Table.objects.all()
        serializer = TableSerializer(tables, many=True)
        return Response(
                {"result": "success", 
                 "data": serializer.data},
                status=status.HTTP_200_OK)


    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Creates a table with given data
        '''
        data = {
            'number': request.data.get('table_number'), 
            'number_of_seats': request.data.get('number_of_seats'),
        }

        serializer = TableSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"result": "Table created successfully", 
                              "data": serializer.validated_data},
                              status=status.HTTP_201_CREATED)

        return Response({"result": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class TableDetailApiView(AdminRoleMixin, APIView):
    '''
    TableDetailApiView:
    to get, update and delete a table
    '''
    permission_classes = [IsAuthenticated]

    def get_object(self, table_number):
        '''
        Helper method to get the object with given table_number
        '''
        try:
            return Table.objects.get(number=table_number)
        except Table.DoesNotExist:
            return None


    def get(self, request, table_number, *args, **kwargs):
        '''
        Retrieves a table with given table_number
        '''
        table = self.get_object(table_number)
        if not table:
            return Response(
                {"result": "Table does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TableSerializer(table)
        return Response(
            {"result": "success", "data": serializer.data },
            status=status.HTTP_200_OK)


    def put(self, request, table_number, *args, **kwargs):
        '''
        Updates the table with given given table_number if exists
        '''
        table = self.get_object(table_number)
        if not table:
            return Response(
                {"result": "Table does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'number_of_seats': request.data.get('number_of_seats'), 
        }
        serializer = TableSerializer(instance = table, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"result": "Table updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK)

        return Response({"result": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, table_number, *args, **kwargs):
        '''
        Deletes the table (soft delete) with given table_number if exists
        '''
        table = self.get_object(table_number)
        if not table:
            return Response(
                {"result": "Table does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        table.delete()
        return Response(
            {"result": "Table has been deleted"},
            status=status.HTTP_200_OK
        )


class ReservationApiListView(generics.ListAPIView):
    '''
    ReservationApiListView
    - Returns a reservations list for today.
    - User can sort the reservation in in ascending or descending order.

    '''
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.filter(date=datetime.datetime.now().date())
    serializer_class = ReservationSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self, *args, **kwargs):
        if(self.request.GET['sort']):
            sort = self.request.GET['sort']
            if (sort == '1'):
                type = "-starting_time"
            else:
                type = "starting_time"

        return super().get_queryset(*args, **kwargs).order_by(type)
        

    def create_reservation_validation(self, data):
        '''
        a reservation validation function which is called when creating a reservation.
        '''
        new_date = data['date']
        new_start_time = data['starting_time']
        new_end_time = data['ending_time']
        table_number = data['table_number']

        # 1. checks if the two times are equals to each other
        if (new_start_time == new_end_time):
            raise Exception(
                "starting time can't be the same as ending time")
        
        # 2. checks if ending is smaller that ending time
        if(new_end_time < new_start_time):
            raise Exception(
                "ending time can't be smaller than statring time")

        # 3. checks if the reservations is within the working hours
        if (new_start_time < starting_woring_time or new_start_time > ending_working_time or
            new_end_time < starting_woring_time or new_end_time > ending_working_time):
            raise Exception(
                "reservation should be with the working hours: " + str(starting_woring_time) + " - " + str(ending_working_time))

        # 4. checking if there is no overlapping
        if (Reservation.objects.filter(date=new_date).filter(
            Q(table__number=table_number) & Q(starting_time__lte=new_start_time) & Q(ending_time__gt=new_start_time) | 
            Q(starting_time__lt=new_end_time) & Q(ending_time__gt=new_end_time)).exists()):
            raise Exception('Sorry, this time slot is reserved, please pick a new time slot')
        
        if (Reservation.objects.filter(date=new_date).filter(
            Q(table__number=table_number) & Q(starting_time__gte=new_start_time) & Q(ending_time__lte=new_end_time)).exists()):
            raise Exception('Sorry, this time slot is reserved, please pick a new time slot')

 
    def post(self, request, *args, **kwargs):
        '''
        Creates a reservation with given data
        '''
        data = {
            'date': request.data.get('date'),
            'starting_time': request.data.get('starting_time'), 
            'ending_time': request.data.get('ending_time'),
            'customer_email': request.data.get('customer_email'),
            'customer_mobile': request.data.get('customer_mobile'),
            'table_number':  request.data.get('table_number')
        }
   

        serializer = CreateReservationSerializer(data=data)
        if serializer.is_valid():
            # get table, if table not exist an exception will be thrown 
            try:
                Table.objects.get(number=serializer.validated_data['table_number'])
            except Table.DoesNotExist:
                return Response(
                    {"result": "Table does not exist" },
                    status=status.HTTP_400_BAD_REQUEST
                    )
                
            try:
                self.create_reservation_validation(serializer.validated_data)

            except Exception as e:
                return Response(
                    {"result": str(e) },
                status=status.HTTP_400_BAD_REQUEST
            )

            serializer.save()
            return Response(
                {"result": "reservation created successfully"},
                status=status.HTTP_201_CREATED)

        return Response({"result": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, starting_time, *args, **kwargs):
        '''
        Deletes the reservation with given starting_time if exists
        '''
        starting_time = datetime.datetime.strptime(str(starting_time), '%H').time()

        reservation = Reservation.objects.filter(
            date=datetime.datetime.now().date(),
            starting_time=starting_time)
        
        if not reservation:
            return Response(
                {"result": "Reservation with starting time of: " + str(starting_time) + "does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        reservation.delete()
        return Response(
            {"result": "reservation has been deleted"},
            status=status.HTTP_200_OK
        )


class AvailableReservationsTimeSlotsView(APIView):
    '''
    AvailableReservationsTimeSlotsView:
    returns the available time slots for reservation for each table.
    '''
    permission_classes = [IsAuthenticated]

    def get(self, request, number_of_seats, *args, **kwargs):
        time_slots = {}
        # 1. get tables with the number of seats:
        tables = Table.objects.filter(number_of_seats=number_of_seats)
        while (len(tables) == 0):
            number_of_seats = number_of_seats +1 
            
            # exit the loop when reaching the max number of seats
            if number_of_seats > max_number_of_seats:
                return Response(
                    {"result": "sorry no suitable table for this number of seats"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            tables = Table.objects.filter(number_of_seats=number_of_seats)

        # 2. get reservations for all the tables 
        for table in tables:
            time_slots[str(table.number)]= []

            reservations = Reservation.objects.filter(table__number=table.number, date=datetime.datetime.now().date()).order_by('starting_time')
            if(len(reservations) > 0):
                # 3. first and last time slot 
                if(starting_woring_time != reservations.first().starting_time):
                    time_slots.get(str(table.number)).append(str(starting_woring_time) + " - " + str(reservations.first().starting_time))
                if(ending_working_time != reservations.last().ending_time ):
                    last_time_slot = str(reservations.last().ending_time) + " - " + str(ending_working_time)

                # 4. caclute the diffrence 
                for index, reservation in enumerate(reservations):
                    try:
                        time_slots.get(str(table.number)).append(
                            str(reservation.ending_time) + " - " + str(reservations[index +1].starting_time))
                    except IndexError:
                        pass 
                time_slots.get(str(table.number)).append(last_time_slot)
    
            else:
                # no previous reservations 
                time_slots.get(str(table.number)).append(str(starting_woring_time) + " - " + str(ending_working_time))
            return Response(
                {"result": "success", 
                 "data": json.loads(json.dumps(time_slots))},
                status=status.HTTP_200_OK)


class ReservationsByFiltersListView(AdminRoleMixin, generics.ListAPIView):
    '''
    ReservationsByFiltersListView:
    returns a paginated list of reservations by the given filters
    '''
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all().order_by('starting_time')
    serializer_class = ReservationSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        '''
        Optionally restricts the returned queryset, by filtering against:
        - tables
        - starting_date
        - ending_date
        '''
        # 
        queryset = super().get_queryset()
        if(self.request.query_params.get('tables')):
            tables = self.request.query_params.get('tables').split(',')
            tables = [int(i) for i in tables]
            queryset = Reservation.objects.filter(table__number__in=tables)

        if(self.request.query_params.get('starting_date')):
            starting_date = self.request.query_params.get('starting_date')
            starting_date = datetime.datetime.strptime(starting_date , '%Y-%m-%d')
            queryset = queryset.filter(date__gte=starting_date)

        if(self.request.query_params.get('ending_date')):
            ending_date = self.request.query_params.get('ending_date')
            ending_date = datetime.datetime.strptime(ending_date , '%Y-%m-%d')
            queryset = queryset.filter(date__lte=ending_date)

        return queryset
