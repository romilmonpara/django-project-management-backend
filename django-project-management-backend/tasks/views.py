from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer
from projects.models import Project
from django_filters.rest_framework import DjangoFilterBackend

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'project', 'assigned_to', 'due_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        project_id = self.request.query_params.get('project')
        if project_id:
            project = Project.objects.get(pk=project_id)
            # Only show tasks if user is a member
            if self.request.user not in project.members.all():
                return queryset.none()
            return queryset.filter(project_id=project_id)
        # Optionally: show only tasks from projects user is a member of
        user_projects = Project.objects.filter(members=self.request.user)
        return queryset.filter(project__in=user_projects)
    
    # extra steps before or after saving
    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        if self.request.user not in project.members.all():
            return Response(
                {'error': 'Only project members can create tasks in this project'}, 
                status=status.HTTP_403_FORBIDDEN)
    
        # NEW CHECK! Only allow assigning tasks to project members
        assigned_to_user = serializer.validated_data.get('assigned_to')
        if assigned_to_user and assigned_to_user not in project.members.all():
            return Response(
                {'error': 'Assigned user must be a member of the project'},
                status=status.HTTP_403_FORBIDDEN)
        serializer.save()

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        task = self.get_object()
        user_id = request.data.get('user_id')

        # Check if the user is a member of the task's project
        project_members = task.project.members.all()
        assign_to_user = None
        try:
            assign_to_user = project_members.get(pk=user_id)
        except Exception:
            return Response({'error': 'User is not a member of this project!'}, status=status.HTTP_403_FORBIDDEN)

        task.assigned_to = assign_to_user
        task.save()
        return Response({'status': 'assigned'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='complete')
    def complete(self, request, pk=None):
        task = self.get_object()
        task.status = 'completed'
        task.save()
        return Response({'status': 'task marked as completed'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, pk=None):
        task = self.get_object()
        if request.method == 'GET':
            comments = task.comments.all()   # Get all comments for this task
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, task=task)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['task', 'user']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
