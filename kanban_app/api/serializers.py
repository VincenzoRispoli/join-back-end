from rest_framework import serializers
from kanban_app.models import Subtask, Contact, Task


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contact model.

    Includes all relevant fields and custom validation for names
    to restrict the presence of specific characters.
    """
    class Meta:
        model = Contact
        fields = [
            'user', 'id', 'first_name', 'last_name',
            'phone', 'email', 'badge_color'
        ]
        extra_kwargs = {
            'email': {'required': False, 'allow_null': True},
            'first_name': {'required': False, 'allow_null': True},
            'last_name': {'required': False, 'allow_null': True},
            'phone': {'required': False, 'allow_null': True}
        }

    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        errors = self.check_contact_data(first_name, last_name, email, phone)

        if errors:
            raise serializers.ValidationError(errors)
        return data

    def check_contact_data(self,first_name, last_name, email, phone):
        errors = {}
        if not first_name:
            errors['first_name'] = 'Please insert a contact first name'
        if not last_name:
            errors['last_name'] = 'Please insert a contact last name'
        if not email:
            errors['email'] = 'Please insert a contact email'
        if not phone:
            errors['phone'] = 'Please insert a phone number'
        return errors


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    Includes:
    - Nested read-only contact data.
    - Write-only field for assigning contacts via primary keys.
    - Computed field for counting associated contacts.
    """
    contacts = ContactSerializer(many=True, read_only=True)
    contacts_ids = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(),
        many=True,
        write_only=True,
        source='contacts'
    )
    contacts_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {
            'title': {'required': False, 'allow_null': True},
            'description': {'required': False, 'allow_null': True},
            'priority': {'required': False, 'allow_null': True},
            'due_date': {'required': False, 'allow_null': True},
            'category': {'required': False}
        }

    def validate(self, data):
        title = data.get('title')
        category = data.get('category')
        date = data.get('due_date')

        errors = self.check_task_data(title, category, date)
        print(errors)
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def check_task_data(self, title, category, date):
        errors = {}
        if not title or len(title) < 4:
            errors['title'] = "The title must have at least 4 characters"

        if date is None:
            errors['due_date'] = 'Please insert the due date'

        if not category:
            errors['category'] = 'Please insert the category'

        return errors

    def get_contacts_count(self, obj):
        """
        Returns the number of contacts related to the task.
        """
        return obj.contacts.count()


class SubtaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subtask model.

    - `task` is a read-only field used for displaying the related task.
    - `task_id` is write-only and used for assigning a subtask to a task.
    """
    task = serializers.PrimaryKeyRelatedField(read_only=True)
    task_id = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(),
        write_only=True,
        source='task'
    )

    class Meta:
        model = Subtask
        fields = ['id', 'task', 'task_id', 'title', 'is_completed']
