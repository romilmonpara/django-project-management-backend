from rest_framework import serializers
from .models import Task, Comment
from django.contrib.auth.models import User

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    class Meta:
        model = Comment
        fields = ['id', 'task', 'user', 'text', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'assigned_to', 'status', 'due_date', 'created_at', 'updated_at', 'comments']
