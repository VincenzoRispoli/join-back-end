from django.db import models
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User

# Create your models here.

class Contact(models.Model):
    """
    Represents a contact person linked to a user account.
    Contacts can be assigned to multiple tasks.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.TextField(max_length=100, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    badge_color = models.CharField(max_length=100, default='red')

    def __str__(self):
        """
        Return the username of the associated user as the string representation.
        """
        return f"{self.first_name} {self.last_name}"


class Task(models.Model):
    """
    Represents a task in the kanban system.
    A task can have multiple contacts assigned and can include subtasks.
    """
    title = models.CharField(max_length=150, blank=True)
    description = models.TextField(max_length=500, blank=True)
    category = models.CharField(max_length=100, blank=True)
    due_date = models.DateField(blank=True, null=True)
    priority = models.CharField(max_length=100)
    contacts = models.ManyToManyField(Contact, related_name='tasks')  # Assigned contacts
    state = models.CharField(max_length=255, default='todo')  # e.g., todo, in-progress, done

    def __str__(self):
        """
        Return the category of the task as the string representation.
        """
        return self.title


class Subtask(models.Model):
    """
    Represents a smaller task that is part of a main task.
    Used to break down work into manageable pieces.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        """
        Return the title of the subtask as the string representation.
        """
        return self.title
    
    
    
