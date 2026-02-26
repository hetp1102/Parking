
from django.db import models
from django.contrib.auth.models import User

class Slot(models.Model):
    number = models.CharField(max_length=10, unique=True)
    is_occupied = models.BooleanField(default=False)
    def __str__(self): return self.number

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    code = models.CharField(max_length=100, unique=True)
    qr_image = models.ImageField(upload_to='qrs/', null=True, blank=True)
    def __str__(self): return f"{self.user.username}-{self.slot.number}"
