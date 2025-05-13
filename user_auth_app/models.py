from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Extension model for the default Django User.

    This model creates a one-to-one relationship with Django’s built-in `User` model,
    allowing you to extend it with additional fields if needed.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns the username of the associated Django user.
        """
        return self.user.username
