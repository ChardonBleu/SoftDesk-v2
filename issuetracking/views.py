from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from issuetracking.models import Project, Issue, Contributor, Comment
from issuetracking.serializers import ProjectSerializer, IssueSerializer
from issuetracking.serializers import ContributorsSerializer, CommentSerializer
from issuetracking.permissions import IsAuthorProject, IsContributorProject, canManageContributors


class ProjectViewSet(viewsets.ModelViewSet):
    """
    The endpoint [project list](/projects/) is the main entry point of the **SoftDesk API**.

    The SoftDesk API is a RESTful API built using Django Rest Framework. It's
    part of project 10 of Openclassrooms formation Pyhton Developpers.

    This API can be used to manage team projects.
    You need to be authenticated to see projects list.
    
    You can signup on [signup endpoint](/signup/).
    Every user can create a new project and then add contributors for this
    project.
    
    You only can see project details if you're author or contributor for this
    project.
    Only projects/issues/comments authors can update or delete projects/issues
    /comments.
    
    On PostMan you'll have to use a [token](/token/) for authentication.
    After the first use of token access you'll have to 
    [refresh](/token/refresh/) it.
    
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthorProject]
    
    def perform_create(self, serializer):
        """The author is automaticaly saved as the authenticated user

        Arguments:
            serializer  -- ProjectSerializer
        """
        serializer.save(author_user=self.request.user)


    def get_queryset(self):
        """This view should return only projects if authenticated user is the
        author or one of the contributors.
        """
        projects_of_user = []
        is_author_or_contrib = Contributor.objects.filter(
            user=self.request.user).values()
        for user in is_author_or_contrib:
            projects_of_user.append(user['project_id'])        
        return Project.objects.filter(id__in=projects_of_user)


class ContributorsViewSet(viewsets.ModelViewSet):

    serializer_class = ContributorsSerializer
    permission_classes = [IsAuthenticated, canManageContributors]

    def get_queryset(self):
        """This view should return a list of all the contributors
        as determined by the project_id portion of the URL.
        """
        project = self.kwargs['project_id']
        return Contributor.objects.filter(project=project)

    def perform_create(self, serializer):
        """When somenone add a contributors he does it for a done project,
        and the project-id is passed in url.

        Arguments:
            serializer  -- CommentSerializer
        """
        project = self.kwargs['project_id']
        project = Project.objects.get(id=project)
        serializer.save(project=project)


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
        project = self.kwargs['project_id']
        project = Project.objects.get(id=project)
        serializer.save(author_user=self.request.user, project=project)
        
    def get_queryset(self):
        """
        This view should return a list of all the issues
        as determined by the project_id portion of the URL.
        """
        project = self.kwargs['project_id']
        return Issue.objects.filter(project=project)


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
        issue = self.kwargs['issue_id']
        issue = Issue.objects.get(id=issue)
        serializer.save(author_user=self.request.user, issue=issue)

    def get_queryset(self):
        """
        This view should return a list of all the comments
        as determined by the issue_id portion of the URL.
        """
        issue = self.kwargs['issue_id']
        return Comment.objects.filter(issue=issue)
