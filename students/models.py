from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Cubicle(models.Model):
    #h_id,h_name,owner ,location,rooms
    name = models.CharField(max_length=30,default="Unizulu Library")
    floor = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    province = models.CharField(max_length=50,default="Kwazul-Natal")
    country = models.CharField(max_length=50,default="South Africa")
    def __str__(self):
        return self.name


class Rooms(models.Model):
    ROOM_STATUS = ( 
    ("1", "available"), 
    ("2", "not available"),    
    ) 

    ROOM_TYPE = ( 
    ("1", "Individual Cubicle"), 
    ("2", "Group Cubicle"),   
    ) 

    #type,no_of_rooms,capacity,prices,Hotel
    room_type = models.CharField(max_length=50,choices = ROOM_TYPE)
    capacity = models.IntegerField()
    Course = models.CharField(max_length=100, default="Introductory Computing")
    size = models.IntegerField()
    hotel = models.ForeignKey(Cubicle, on_delete = models.CASCADE)
    status = models.CharField(choices =ROOM_STATUS,max_length = 15)
    roomnumber = models.IntegerField()
    def __str__(self):
        return self.hotel.name

class Reservation(models.Model):

    check_in = models.TimeField(auto_now =False)
    check_out = models.TimeField()
    room = models.ForeignKey(Rooms, on_delete = models.CASCADE)
    guest = models.ForeignKey(User, on_delete= models.CASCADE)
    
    booking_id = models.CharField(max_length=100,default="null")
    def __str__(self):
        return self.guest.username

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    feedback = models.TextField()
    rating = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

