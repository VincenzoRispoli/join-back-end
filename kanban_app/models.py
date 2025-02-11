from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.TextField(max_length=100)
    phone = models.CharField(max_length=200)
    badge_color = models.CharField(max_length=100, default='red')
    
    def __str__(self):
        return self.user.username
    
    
class Task(models.Model):
    title = models.CharField(max_length = 150)
    description = models.TextField(max_length = 500)
    category = models.CharField(max_length = 100)
    due_date = models.DateField()
    priority = models.CharField(max_length = 100)
    contacts = models.ManyToManyField(Contact, related_name = 'tasks')
    state = models.CharField(max_length=255, default='todo')
    
    def __str__(self):
        return self.category
    
    
class Subtask(models.Model):
      task = models.ForeignKey(Task, on_delete = models.CASCADE, related_name = 'subtasks')
      title = models.CharField(max_length = 200)
      is_completed = models.BooleanField(default = False)
      
      def __str__(self):
          return self.title
    
    
    
