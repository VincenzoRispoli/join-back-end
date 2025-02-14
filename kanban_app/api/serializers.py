from rest_framework import serializers
from kanban_app.models import Subtask, Contact, Task

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields= ['user', 'id','first_name','last_name','phone', 'email','badge_color']
        
    def validate_name(self, value):
        errors = []
        if 'X' in value:
          errors.append('No X in name please')
        if 'Y' in value:
          errors.append('No Y in name please')
        
        if errors:
            raise serializers.ValidationError(errors)
        return value

    


class TaskSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)
    contacts_ids = serializers.PrimaryKeyRelatedField(
        queryset = Contact.objects.all(),
        many=True,
        write_only=True,
        source='contacts' # 'users' si riferisce alla variabile users creata nella prima riga del TaskDetailSerialiezer
    )
    contacts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = '__all__'
        
    
    def get_contacts_count(self, obj):
        return obj.contacts.count()
      
      
class TaskHyperLinkedSerializer(TaskSerializer, serializers.HyperlinkedModelSerializer):
    
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    
    class Meta:
        model = Task
        exclude = []


class SubtaskSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(read_only=True)
    task_id = serializers.PrimaryKeyRelatedField(
        queryset= Task.objects.all(),
        write_only=True,
        source='task')
    class Meta:
        model = Subtask
        fields = ['id','task','task_id', 'title', 'is_completed']
    