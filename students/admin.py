from django.contrib import admin
from .models import Cubicle,Rooms,Reservation,Feedback
# Register your models here.



admin.site.register(Cubicle)
admin.site.register(Rooms)
admin.site.register(Reservation)
admin.site.register(Feedback)