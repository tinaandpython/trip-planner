from django.db import models
from django.contrib.auth.models import User

class ItineraryGenerator(models.Model):
    # The on_delete=models.CASCADE argument ensures that if a user is deleted, all their associated trip plans are also deleted.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.CharField(max_length=255)
    day = models.IntegerField()
    plan = models.TextField()

    def __str__(self):
        return f"{self.destination} - Day {self.day}"


