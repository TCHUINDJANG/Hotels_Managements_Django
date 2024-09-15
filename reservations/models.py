from django.db import models

# Create your models here.

from django.db import models
from rooms.models import Room

class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=100)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation by {self.guest_name} for Room {self.room.number}"
