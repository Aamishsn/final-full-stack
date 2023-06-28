# from django.http import HttpResponse
import json
from django.shortcuts import render

from .models import MenuItem
from django.core import serializers
from .models import Booking
from datetime import datetime
from .forms import BookingForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
# from .forms import BookingForm


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'book.html', context)

# Add code for the bookings() view


def menu(request):
    menu_data = MenuItem.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None):
    if pk:
        menu_item = MenuItem.objects.get(pk=pk)
    else:
        menu_item = ""
    return render(request, 'menu_item.html', {"menu_item": menu_item})


@csrf_exempt
def bookings(request):
    if request.method == "POST":
        data = json.load(request)
        exist = Booking.objects.filter(
            reservation_date=data['reservation_date']).filter(reservation_slot=data['reservation_slot']).exists()

        if not exist:
            booking = Booking(
                first_name=data['first_name'], reservation_date=data['reservation_date'], reservation_slot=data['reservation_slot'])
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
    date = request.GET.get('date', datetime.today().date())
    bookings_date = Booking.objects.all().filter(reservation_date=date)
    booking_date_json = serializers.serialize('json', bookings_date)
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html', {"bookings": booking_json, "bookings_date": booking_date_json})


@csrf_exempt
def bookings_date(request):
    if request.method == 'POST':
        data = json.load(request)
        exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
            reservation_slot=data['reservation_slot']).exists()
        if exist == False:
            booking = Booking(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')

    date = request.GET.get('date', datetime.today().date())

    bookings = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(booking_json, content_type='application/json')
