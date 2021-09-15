from django.utils.translation import gettext_lazy as _
from django.db import models
from account.models import User


class Project(models.Model):
    """Projects table"""

    TYPE = [
        ("BACK", "Back-end"),
        ("FRONT", "Front-end"),
        ("IOS", "iOS"),
        ("ANDROID", "Android"),
    ]

    title = models.CharField(
        "project title",
        max_length=255,
        help_text=_("Each project has a title with max 255 caracters."),
    )
    description = models.CharField(
        "project description",
        max_length=2048,
        help_text=_("Each project has a description"),
    )
    type = models.CharField(
        "Project type",
        max_length=7,
        help_text=_(
            "Each project has a type wich can be Back-end, Front-end, \
            iOS or Android"
        ),
        choices=TYPE,
    )
    author_user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text=_(
            "Each project has an author wich is a custom user. Each \
            user can have several projects"
        ),
        verbose_name="related user (author)",
        related_name='projects',
    )


    class Meta:
        ordering = ['id']


    def save(self, *args, **kwargs):
        """Override save of the current instance of Project when create a new
        project. Call a Contributor method :
        save_author_project_as_contributor()
        """
        super(Project, self).save(*args, **kwargs)
        Contributor.save_author_project_as_contributor(self)


class Contributor(models.Model):
    """Contributors table"""

    PERMISSION = [("CONTRIB", "Contributeur"), ("AUTHOR", "Auteur")]

    permission = models.CharField(
        "Contributor permission",
        choices=PERMISSION,
        max_length=7,
        help_text=_(
            "A simple contributor can read everything on project, \
            issues, comments, he can create issues and commetns but he can't \
                delete or update project, issues or comments. An author can \
                    Update and delete everything he created."
        ),
    )
    role = models.CharField(
        "Contributor role",
        max_length=255,
        help_text=_(" "),
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text=_(
            "Each contributor is a custom user. A user can contribute \
            to several projects. A user can be a simple contributor or the \
                project author"
        ),
        verbose_name="related user (project contributor or author)",
        related_name='contributors'
    )
    project_id = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        help_text=_(
            "Each project has sevaral contributors. One of them is the \
            project author (permission)."
        ),
        verbose_name="related projects",
    )


    class Meta:
        ordering = ['id']

    @classmethod
    def save_author_project_as_contributor(cls, project):
        """Create a contributor as an AUTHOR when the authenticated user
        create a new project.
        get_or_create method prevents to duplicate contributor when updating
        project instead of creting it.

        Arguments:
            project {Project Object} -- Project object
        """
        cls.objects.get_or_create(permission='AUTHOR', user_id=project.author_user_id, project_id=project)
    
    @classmethod
    def save_assignee_issue_as_contributor(cls, issue):
        """Create a contributor as a CONTRIB when the authenticated user
        create a new issue with an assignee_user.
        get_or_create method prevents to duplicate contributor when updating
        project instead of creting it.

        Arguments:
            project {Project Object} -- Project object
        """
        cls.objects.get_or_create(permission='CONTRIB', user_id=issue.assignee_user_id, project_id=issue.project_id)

class Issue(models.Model):
    """Issues table"""

    TAG = [("BUG", "Bug"), ("IMPROV", "Améliorations"), ("TASK", "Tâche")]
    PRIORITY = [("LOW", "Faible"), ("MEDIUM", "Moyenne"), ("HIGH", "Elevée")]
    STATUS = [("TODO", "A faire"), ("DEV", "En cours"), ("DONE", "Terminé")]

    title = models.CharField(
        "Issue title",
        max_length=255,
        help_text=_("Each issue has a title with 255 characters max."),
    )
    description = models.CharField(
        "Issue description",
        max_length=2048,
        help_text=_("Each issue has a description."),
    )
    tag = models.CharField(
        "Issue tag",
        help_text=_("Each issue has a tag between: BUG, IMPROVEMENT, TASK"),
        max_length=6,
        choices=TAG,
    )
    priority = models.CharField(
        "Issue priority",
        help_text=_("Each issue has a priority between: LOW, MEDIUM, HIGH"),
        max_length=6,
        choices=PRIORITY,
    )
    project_id = models.ForeignKey(
        "Project",
        help_text=_(
            "Each issue has a project. A project can have several \
            issues"
        ),
        on_delete=models.CASCADE,
        verbose_name="project issue",
        related_name="issues",
    )
    status = models.CharField(
        "Issue status",
        help_text=_("Each issue has a tag between: TODO, DEV, DONE"),
        max_length=4,
        choices=STATUS,
    )
    author_user_id = models.ForeignKey(
        User,
        help_text=_(
            "Each issue has an author. A custom user can have several \
            issues"
        ),
        on_delete=models.CASCADE,
        verbose_name="author issue",
        related_name="issues",
    )
    assignee_user_id = models.ForeignKey(
        User,
        help_text=_(
            "Each issue has an assignee. By default asssignee is the \
            author"
        ),
        on_delete=models.CASCADE,
        verbose_name="assignee issue",
        default=author_user_id,
        related_name="issues_assign",
    )
    created_datetime = models.DateTimeField(
        "Created datetime issue",
        auto_now_add=True,
        help_text=_("issue creation date is automatically filled in."),
    )


    class Meta:
        ordering = ['created_datetime']


    def save(self, *args, **kwargs):
        """Override save of the current instance of Issue when create a new
        issue. Call a Contributor method :
        save_assignee_issue_as_contributor()
        """
        super(Issue, self).save(*args, **kwargs)
        if self.assignee_user_id != self.author_user_id:
            Contributor.save_assignee_issue_as_contributor(self)


class Comment(models.Model):
    """Comments table"""

    description = models.CharField(
        "Comment description",
        max_length=2048,
        help_text=_("Each comment has a description."),
    )
    author_user_id = models.ForeignKey(
        User,
        help_text=_(
            "Each comment has an author. A custom user can have several \
            comments"
        ),
        on_delete=models.CASCADE,
        verbose_name="author comment",
        related_name='comments',
    )
    issue_id = models.ForeignKey(
        "Issue",
        help_text=_(
            "Each comment has an issue. An issue can have several \
            comments"
        ),
        on_delete=models.CASCADE,
        verbose_name="issue comment",
        related_name="comments",
    )
    created_datetime = models.DateTimeField(
        "Created datetime comments",
        auto_now_add=True,
        help_text=_("comment creation date is automatically filled in."),
    )

    class Meta:
        ordering = ['created_datetime']
