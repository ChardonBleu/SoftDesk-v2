from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from issuetracking.models import Project, Issue, Contributor, Comment
from issuetracking.serializers import ProjectSerializer, IssueSerializer
from issuetracking.serializers import ContributorsSerializer, CommentSerializer
from issuetracking.permissions import IsAuthorProject, IsContributorProject


class ProjectViewSet(viewsets.ModelViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthorProject]
    
    def perform_create(self, serializer):
        """The author is automaticaly saved as the authenticated user

        Arguments:
            serializer  -- ProjectSerializer
        """
        serializer.save(author_user_id=self.request.user)


class ContributorsViewSet(viewsets.ModelViewSet):

    serializer_class = ContributorsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """This view should return a list of all the contributors
        as determined by the project_id portion of the URL.
        """
        project_id = self.kwargs['project_id']
        return Contributor.objects.filter(project_id=project_id)


class IssueViewSet(viewsets.ModelViewSet):

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsContributorProject]   
    
    
    def perform_create(self, serializer):
        """The author is automaticaly saved as the authenticated user.
        The project_id is authomaticaly saved using the project_id in the url
        endpoint.

        Arguments:
            serializer  -- CommentSerializer
        """
        project_id = self.kwargs['project_id']
        project = Project.objects.get(id=project_id)
        serializer.save(author_user_id=self.request.user, project_id=project)
        
    def get_queryset(self):
        """
        This view should return a list of all the issues
        as determined by the project_id portion of the URL.
        """
        project_id = self.kwargs['project_id']
        return Issue.objects.filter(project_id=project_id)


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsContributorProject]

    def perform_create(self, serializer):
        """The author is automaticaly saved as the authenticated user.
        The issue_id is authomaticaly saved using the issue_id in the url
        endpoint. 

        Arguments:
            serializer  -- CommentSerializer
        """
        issue_id = self.kwargs['issue_id']
        issue = Issue.objects.get(id=issue_id)
        serializer.save(author_user_id=self.request.user, issue_id=issue)

    def get_queryset(self):
        """
        This view should return a list of all the comments
        as determined by the issue_id portion of the URL.
        """
        issue_id = self.kwargs['issue_id']
        return Comment.objects.filter(issue_id=issue_id)
