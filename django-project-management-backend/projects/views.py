from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Project
from .serializers import ProjectSerializer
from django.contrib.auth.models import User

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'created_by', 'members']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, members=[self.request.user])

    @action(detail=True, methods=['post'], url_path='add-member')
    def add_member(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            project.members.add(user)
            return Response({'status': 'member added'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='complete')
    def complete(self, request, pk=None):
        project = self.get_object()
        # Only creator can complete the project
        if project.created_by != request.user:
            return Response({'error': 'Only creator can complete this project'}, status=status.HTTP_403_FORBIDDEN)
        project.status = 'completed'
        project.save()
        return Response({'status': 'project marked as completed'}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        if project.created_by != request.user:
            return Response({'error': 'Only creator can delete'}, status=403)
        project.delete()
        return Response({'success': 'Project deleted successfully'}, status=status.HTTP_200_OK)
