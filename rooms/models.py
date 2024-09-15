from django.db import models

# Create your models here.

class Room(models.Model):
    ROOM_TYPES = [
        ('S', 'Single'),
        ('D', 'Double'),
        ('T', 'Triple'),
    ]

    number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=1,choices=ROOM_TYPES)
    price_night = models.DecimalField(max_digits=10, decimal_places=2)
    is_avaiable = models.BooleanField(default=True)


    def __str__(self):
        return f"Room {self.number} ({self.get_room_type_display})"