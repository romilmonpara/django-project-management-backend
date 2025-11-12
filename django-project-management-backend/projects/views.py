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
        # Only project creator can add members
        if project.created_by != request.user:
            return Response({'error': 'Only the project creator can add members.'},
                            status=status.HTTP_403_FORBIDDEN)
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'User ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        project.members.add(user)
        return Response({'status': 'Member added successfully.'}, status=status.HTTP_200_OK)

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
        # Only creator can delete the project
        project = self.get_object()
        if project.created_by != request.user:
            return Response({'error': 'Only creator can delete'}, status=403)
        project.delete()
        return Response({'success': 'Project deleted successfully'}, status=status.HTTP_200_OK)
