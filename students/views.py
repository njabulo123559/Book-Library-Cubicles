from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Cubicle, Rooms, Reservation, Student
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from datetime import time
from .forms import FeedbackForm
from django.db.models import Q
# Create your views here.

# homepage


def homepage(request):
    all_location = Cubicle.objects.values_list(
        'location', 'id').distinct().order_by()

    if request.method == "POST":
        try:
            print(request.POST)
            hotel = Cubicle.objects.get(
                id=int(request.POST['search_location']))
            rr = []

            # Convert user input to time objects
            cin_parts = request.POST['check_in'].split(':')
            cin = time(int(cin_parts[0]), int(cin_parts[1]))

            cout_parts = request.POST['check_out'].split(':')
            cout = time(int(cout_parts[0]), int(cout_parts[1]))

            # Find reservations that overlap with the requested check-in and check-out times
            for each_reservation in Reservation.objects.all():
                if each_reservation.check_in < cin and each_reservation.check_out < cout:
                    pass
                elif each_reservation.check_in > cin and each_reservation.check_out > cout:
                    pass
                else:
                    rr.append(each_reservation.room.id)

            room = Rooms.objects.filter(hotel=hotel, capacity__gte=int(
                request.POST['capacity'])).exclude(id__in=rr)

            if len(room) == 0:
                messages.warning(
                    request, "Sorry, no cubicles are available during this time period.")

            data = {'rooms': room, 'all_location': all_location, 'flag': True}
            response = render(request, 'index.html', data)
        except Exception as e:
            messages.error(request, str(e))
            response = render(request, 'index.html', {
                              'all_location': all_location})
    else:
        data = {'all_location': all_location}
        response = render(request, 'index.html', data)

    return HttpResponse(response)

# about


def aboutpage(request):
    return HttpResponse(render(request, 'about.html'))

# contact page


def contactpage(request):
    return HttpResponse(render(request, 'contact.html'))

# user sign up


def user_sign_up(request):
    if request.method == "POST":
        user_name = request.POST['username']
        email1 = request.POST['email']
        first_name = request.POST['name']

        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.warning(request, "Password didn't matched")
            return redirect('userloginpage')

        try:
            if User.objects.all().get(username=user_name):
                messages.warning(request, "Student Number is Not Available")
                return redirect('userloginpage')
        except:
            pass

        new_user = User.objects.create_user(
            username=user_name, password=password1, email=email1, first_name=first_name)
        new_user.is_superuser = False
        new_user.is_staff = False
        new_user.save()
        messages.success(request, "Registration Successfull")
        return redirect("userloginpage")
    return HttpResponse('Access Denied')
# staff sign up


def staff_sign_up(request):
    if request.method == "POST":
        user_name = request.POST['username']

        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.success(request, "Password didn't Matched")
            return redirect('staffloginpage')
        try:
            if User.objects.all().get(username=user_name):
                messages.warning(request, "Username Already Exist")
                return redirect("staffloginpage")
        except:
            pass

        new_user = User.objects.create_user(
            username=user_name, password=password1)
        new_user.is_superuser = False
        new_user.is_staff = True
        new_user.save()
        messages.success(request, " Staff Registration Successfull")
        return redirect("staffloginpage")
    else:

        return HttpResponse('Access Denied')
# user login and signup page


def user_log_sign_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pswd']

        user = authenticate(username=email, password=password)
        try:
            if user.is_staff:

                messages.error(request, "Incorrect username or Password")
                return redirect('staffloginpage')
        except:
            pass

        if user is not None:
            login(request, user)
            messages.success(request, "successful logged in")
            print("Login successfull")
            return redirect('homepage')
        else:
            messages.warning(request, "Incorrect username or password")
            return redirect('userloginpage')

    response = render(request, 'user/userlogsign.html')
    return HttpResponse(response)

# logout for admin and user


def logoutuser(request):
    if request.method == 'GET':
        logout(request)
        messages.success(request, "Logged out successfully")
        print("Logged out successfully")
        return redirect('homepage')
    else:
        print("logout unsuccessfull")
        return redirect('userloginpage')

# staff login and signup page


def staff_log_sign_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user.is_staff:
            login(request, user)
            return redirect('staffpanel')

        else:
            messages.success(request, "Incorrect username or password")
            return redirect('staffloginpage')
    response = render(request, 'staff/stafflogsign.html')
    return HttpResponse(response)

# staff panel page


@login_required(login_url='/staff')
def panel(request):

    if request.user.is_staff == False:
        return HttpResponse('Access Denied')

    rooms = Rooms.objects.all()
    total_rooms = len(rooms)
    available_rooms = len(Rooms.objects.all().filter(status='1'))
    unavailable_rooms = len(Rooms.objects.all().filter(status='2'))
    reserved = len(Reservation.objects.all())

    hotel = Cubicle.objects.values_list('location', 'id').distinct().order_by()

    response = render(request, 'staff/panel.html', {'location': hotel, 'reserved': reserved, 'rooms': rooms,
                      'total_rooms': total_rooms, 'available': available_rooms, 'unavailable': unavailable_rooms})
    return HttpResponse(response)

# for editing room information


@login_required(login_url='/staff')
def edit_room(request):
    if request.user.is_staff == False:
        return HttpResponse('Access Denied')
    if request.method == 'POST' and request.user.is_staff:
        print(request.POST)
        old_room = Rooms.objects.all().get(id=int(request.POST['roomid']))
        hotel = Cubicle.objects.all().get(id=int(request.POST['hotel']))
        old_room.room_type = request.POST['roomtype']
        old_room.capacity = int(request.POST['capacity'])
        old_room.course = request.POST['price']
        old_room.size = int(request.POST['size'])
        old_room.hotel = hotel
        old_room.status = request.POST['status']
        old_room.room_number = int(request.POST['roomnumber'])

        old_room.save()
        messages.success(request, "Cubicles Details Updated Successfully")
        return redirect('staffpanel')
    else:

        room_id = request.GET['roomid']
        room = Rooms.objects.all().get(id=room_id)
        response = render(request, 'staff/editroom.html', {'room': room})
        return HttpResponse(response)

# for adding room


@login_required(login_url='/staff')
def add_new_room(request):
    if request.user.is_staff == False:
        return HttpResponse('Access Denied')
    if request.method == "POST":
        new_room = Rooms()
        hotel = Cubicle.objects.all().get(id=int(request.POST['hotel']))
        print(f"id={hotel.id}")
        print(f"name={hotel.name}")

        new_room.roomnumber = request.POST['number']
        new_room.room_type = request.POST['roomtype']
        new_room.capacity = int(request.POST['capacity'])
        new_room.size = int(request.POST['size'])
        new_room.capacity = int(request.POST['capacity'])
        new_room.hotel = hotel
        new_room.status = request.POST['status']

        new_room.save()
        messages.success(request, "New Cubicle Added Successfully")

    return redirect('staffpanel')

# booking room page


@login_required(login_url='/user')
def book_room_page(request):
    room = Rooms.objects.all().get(id=int(request.GET['roomid']))
    return HttpResponse(render(request, 'user/bookroom.html', {'room': room}))

# For booking the room


@login_required(login_url='/user')
def book_room(request):

    if request.method == "POST":

        room_id = request.POST['room_id']

        room = Rooms.objects.all().get(id=room_id)
        # for finding the reserved rooms on this time period for excluding from the query set
        for each_reservation in Reservation.objects.all().filter(room=room):
            if str(each_reservation.check_in) < str(request.POST['check_in']) and str(each_reservation.check_out) < str(request.POST['check_out']):
                pass
            elif str(each_reservation.check_in) > str(request.POST['check_in']) and str(each_reservation.check_out) > str(request.POST['check_out']):
                pass
            else:
                messages.warning(
                    request, "Sorry This Cubicle is unavailable for Booking")
                return redirect("homepage")

        if 'submit_action' in request.POST:

            user_email = request.POST['email']
            user_name = request.POST['username']
            user_time = request.POST['check_in']

            current_user = request.user

            # send email
            subject = 'Cubicle Booked'
            message = f'Hello {user_name},  This is to notify you that your cubicle,  has been booked successfully.!!\n\n  Please make sure to check-in via the front desk before {user_time}\n\nThank You. '
            recipient_list = [user_email]

            send_mail(subject, message, settings.EMAIL_HOST_USER,
                      recipient_list, fail_silently=False)

        current_user = request.user
        total_person = int(request.POST['person'])
        booking_id = str(room_id) + str(datetime.datetime.now())

        reservation = Reservation()
        room_object = Rooms.objects.all().get(id=room_id)
        room_object.status = '2'

        user_object = User.objects.all().get(username=current_user)

        reservation.guest = user_object
        reservation.room = room_object
        person = total_person
        reservation.check_in = request.POST['check_in']
        reservation.check_out = request.POST['check_out']

        reservation.save()

        messages.success(request, "Congratulations! Booking Successfull")

        return redirect("homepage")
    else:
        return HttpResponse('Access Denied')


def handler404(request):
    return render(request, '404.html', status=404)


@login_required(login_url='/staff')
def view_room(request):
    room_id = request.GET['roomid']
    room = Rooms.objects.all().get(id=room_id)

    reservation = Reservation.objects.all().filter(room=room)
    return HttpResponse(render(request, 'staff/viewroom.html', {'room': room, 'reservations': reservation}))


@login_required(login_url='/user')
def user_bookings(request):
    if request.user.is_authenticated == False:
        return redirect('userloginpage')
    user = User.objects.all().get(id=request.user.id)
    print(f"request user id ={request.user.id}")
    bookings = Reservation.objects.all().filter(guest=user)
    if not bookings:
        messages.warning(request, "No Bookings Found")
    return HttpResponse(render(request, 'user/mybookings.html', {'bookings': bookings}))


@login_required(login_url='/staff')
def add_new_location(request):
    if request.method == "POST" and request.user.is_staff:
        floor = request.POST['new_owner']
        location = request.POST['new_city']
        province = request.POST['new_state']
        country = request.POST['new_country']

        hotels = Cubicle.objects.all().filter(location=location, province=province)
        if hotels:
            messages.warning(
                request, "Sorry City at this Location already exist")
            return redirect("staffpanel")
        else:
            new_hotel = Cubicle()
            new_hotel.floor = floor
            new_hotel.location = location
            new_hotel.province = province
            new_hotel.country = country
            new_hotel.save()
            messages.success(
                request, "New Location Has been Added Successfully")
            return redirect("staffpanel")

    else:
        return HttpResponse("Not Allowed")

# for showing all bookings to staff


@login_required(login_url='/staff')
def all_bookings(request):

    bookings = Reservation.objects.all()
    if not bookings:
        messages.warning(request, "No Bookings Found")
    return HttpResponse(render(request, 'staff/allbookings.html', {'bookings': bookings}))


@login_required(login_url='/user')
def send_email(request):
    if request.method == "POST":
        user_email = request.POST['email']
        user_name = request.POST['username']
        user_time = request.POST['check_in']

        # send email
        subject = 'Cubicle Booked'
        message = f'Hello {user_name},  This is to notify you that your cubicle has been booked successfully.!!      Please make to sure to check-in via the front desk before {user_time} '
        recipient_list = [user_email]

        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  recipient_list, fail_silently=False)

        return redirect('homepage')

    return render(request, 'user/bookroom.html')


@login_required(login_url='/user')
def feedback_form(request):
    if request.method == 'POST':
        # If the form has been submitted, process the data
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('homepage')

    else:
        # If it's a GET request, display an empty form
        form = FeedbackForm()

    return render(request, 'user/feedback_form.html', {'form': form})
