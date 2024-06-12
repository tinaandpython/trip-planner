from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

class ItineraryGenerator(models.Model):
    # The on_delete=models.CASCADE argument ensures that if a user is deleted, all their associated trip plans are also deleted.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.CharField(max_length=255)
    api_response = JSONField(default={}) # default is set to empty to cover the database entries with the previous layout that has no API response

    def __str__(self):
        return f"{self.destination} - api_response {self.api_response}"


