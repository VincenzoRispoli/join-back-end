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
    
    # def create(self, validated_data):
    #     return User.objects.create(**validated_data)
    
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.phone = validated_data.get('phone', instance.phone)
    #     instance.badgeColor = validated_data.get('badgeColor', instance.badgeColor)
    #     instance.save()
    #     return instance


    


class TaskSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)
    # users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # users = serializers.StringRelatedField(many=True, read_only=True)
    # users = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name= 'user-detail')
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

# class TaskDetailSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only = True)
#     title = serializers.CharField(max_length = 150)
#     description = serializers.CharField(max_length = 500)
#     category = serializers.CharField(max_length = 100)
#     due_date = serializers.DateField()
#     priority = serializers.CharField(max_length = 100)
#     users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#     status = serializers.CharField(max_length = 100)
    
    


# class TaskCreateSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length = 150)
#     description = serializers.CharField(max_length = 500)
#     category = serializers.CharField(max_length = 100)
#     due_date = serializers.DateField()
#     priority = serializers.CharField(max_length = 100)
#     users = serializers.ListField(child=serializers.IntegerField(),write_only=True)
#     status = serializers.CharField(max_length = 100)
    
#     def validate_users(self, value):
#         users = User.objects.filter(id__in=value)
#         if len(users) != len(value):
#             raise serializers.ValidationError('Some user ids not found')
#         return value
    
#     def create(self, validated_data):
#         user_ids = validated_data.pop('users')
#         task = Task.objects.create(**validated_data)
#         users = User.objects.filter(id__in=user_ids)
#         task.users.set(users)
#         return task
    
#     def update(self, instance, validated_data):
#         users_ids = validated_data.pop('users')
#         users = User.objects.filter(id__in=users_ids)
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.category = validated_data.get('category', instance.category)
#         instance.due_date = validated_data.get('due_date', instance.due_date)
#         instance.priority = validated_data.get('priority', instance.priority)
#         instance.status = validated_data.get('status', instance.status)
#         instance.users.set(users)
#         instance.save()
#         return instance

class SubtaskSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(read_only=True)
    task_id = serializers.PrimaryKeyRelatedField(
        queryset= Task.objects.all(),
        write_only=True,
        source='task')
    class Meta:
        model = Subtask
        fields = ['id','task','task_id', 'title', 'is_completed']
    