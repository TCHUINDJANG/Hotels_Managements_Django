from django.db import models 
from django.contrib.auth.models import User 
from phonenumber_field.modelfields import PhoneNumberField
# from  .models import Booking
from .models import *
# from hotel.models import Booking

 

# Create your models here.


class Guest(models.Model):
    user = models.OneToOneField(User , null=True, on_delete=models.CASCADE)
    phoneNumberssds = PhoneNumberField(unique=True)

    def __str__(self):
        return str(self.user)
    

    def numOfBooking(self):
        return Booking.objects.filter(guets=self).count()
    
    def numOfDays(self):
        totalDay = 0
        bookings = bookings.objects.filter(guest=self)
        for b in bookings:
            day = b.endDate - b.startDate
            totalDay+=int(day.days)
        return totalDay
    

    def numOfLastBookingDay(self):
        try:
            return int((Booking.objects.filter(guest=self).last().endDate - Booking.objects.filter(guest=self).last().startDate).days)
        except:
            return 0
        
    def currentRoom(self):
        booking = Booking.objects.filter(guest=self).last()
        return booking.number


class Employee(models.Model):
    user = models.OneToOneField(User, null=True , on_delete=models.CASCADE)
    phoneNumber = PhoneNumberField(unique=True)
    salary = models.FloatField()

    def __str__(self):
        return str(self.user)
    

class Task(models.Model):
    employe = models.ForeignKey(Employee, null=True , on_delete=models.CASCADE)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    description = models.TextField()

    def str(self):
        return str(self.employee)