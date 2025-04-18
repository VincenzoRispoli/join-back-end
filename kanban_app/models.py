from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Contact(models.Model):
    """
    Represents a contact person linked to a user account.
    Contacts can be assigned to multiple tasks.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.TextField(max_length=100)
    phone = models.CharField(max_length=200)
    badge_color = models.CharField(max_length=100, default='red')

    def __str__(self):
        """
        Return the username of the associated user as the string representation.
        """
        return self.user.username


class Task(models.Model):
    """
    Represents a task in the kanban system.
    A task can have multiple contacts assigned and can include subtasks.
    """
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    category = models.CharField(max_length=100)
    due_date = models.DateField()
    priority = models.CharField(max_length=100)
    contacts = models.ManyToManyField(Contact, related_name='tasks')  # Assigned contacts
    state = models.CharField(max_length=255, default='todo')  # e.g., todo, in-progress, done

    def __str__(self):
        """
        Return the category of the task as the string representation.
        """
        return self.category


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
    
    
    
