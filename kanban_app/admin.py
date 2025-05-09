from django.contrib import admin
from .models import Contact, Task, Subtask

# Register your models here.

admin.site.register(Contact)
admin.site.register(Task)
admin.site.register(Subtask)
