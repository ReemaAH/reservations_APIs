from django.conf.urls import url
from django.urls import include, path

from .views import (
    AvailableReservationsTimeSlotsView, ReservationApiListView,
    ReservationsByFiltersListView, TableApiListView, TableDetailApiView,
)

urlpatterns = [
    path('',  ReservationApiListView.as_view()),
    path('<str:customer_mobile>/',  ReservationApiListView.as_view()),
    path('time-slots/<int:number_of_seats>/', AvailableReservationsTimeSlotsView.as_view()),
    path('all/', ReservationsByFiltersListView.as_view()),
    path('tables', TableApiListView.as_view()),
    path('tables/<int:table_number>/', TableDetailApiView.as_view()),


]
