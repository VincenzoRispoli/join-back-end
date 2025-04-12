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

    def validate_name(self, value):
        """
        Custom validation method (unused currently).

        NOTE: This method would only be called if 'name' was a field in the serializer,
        which it isn't. You may want to use `validate_first_name` and `validate_last_name` instead.
        """
        errors = []
        if 'X' in value:
            errors.append('No X in name please')
        if 'Y' in value:
            errors.append('No Y in name please')

        if errors:
            raise serializers.ValidationError(errors)

        return value


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

    def get_contacts_count(self, obj):
        """
        Returns the number of contacts related to the task.
        """
        return obj.contacts.count()


class TaskHyperLinkedSerializer(TaskSerializer, serializers.HyperlinkedModelSerializer):
    """
    Extends TaskSerializer using HyperlinkedModelSerializer
    to use hyperlinks for related fields instead of primary keys.

    Optionally allows dynamic field inclusion by passing a `fields` argument.
    """
    def __init__(self, *args, **kwargs):
        
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            # Remove fields not explicitly listed
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Task
        exclude = [] 


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