from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from account.models import User
from issuetracking.models import Project, Issue, Contributor, Comment


class CommentSerializer(serializers.ModelSerializer):

    author_user = serializers.SlugRelatedField(read_only=True,
                                               slug_field='username')
    issue = serializers.SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author_user',
                  'issue', 'created_datetime']


class IssueSerializer(serializers.ModelSerializer):

    comments = StringRelatedField(many=True, read_only=True)
    author_user = serializers.SlugRelatedField(read_only=True,
                                               slug_field='username')
    assignee_user = serializers.SlugRelatedField(queryset=User.objects.all(),
                                                 slug_field='username')
    project = serializers.SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'project',
                  'status', 'author_user', 'assignee_user',
                  'created_datetime', 'comments']


class ContributorsSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(),
                                        slug_field='username')
    project = serializers.SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        model = Contributor
        fields = ['id', 'permission', 'role', 'user', 'project']


class ProjectSerializer(serializers.ModelSerializer):

    issues = StringRelatedField(many=True, read_only=True)
    contributors = ContributorsSerializer(many=True, read_only=True)
    author_user = serializers.SlugRelatedField(read_only=True,
                                               slug_field='username')

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type',
                  'author_user', 'contributors', 'issues']
