# Generated by Django 3.2.7 on 2021-09-15 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Each project has a title with max 255 caracters.', max_length=255, verbose_name='project title')),
                ('description', models.CharField(help_text='Each project has a description', max_length=2048, verbose_name='project description')),
                ('type', models.CharField(choices=[('BACK', 'Back-end'), ('FRONT', 'Front-end'), ('IOS', 'iOS'), ('ANDROID', 'Android')], help_text='Each project has a type wich can be Back-end, Front-end,             iOS or Android', max_length=7, verbose_name='Project type')),
                ('author_user_id', models.ForeignKey(help_text='Each project has an author wich is a custom user. Each             user can have several projects', on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL, verbose_name='related user (author)')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Each issue has a title with 255 characters max.', max_length=255, verbose_name='Issue title')),
                ('description', models.CharField(help_text='Each issue has a description.', max_length=2048, verbose_name='Issue description')),
                ('tag', models.CharField(choices=[('BUG', 'Bug'), ('IMPROV', 'Améliorations'), ('TASK', 'Tâche')], help_text='Each issue has a tag between: BUG, IMPROVEMENT, TASK', max_length=6, verbose_name='Issue tag')),
                ('priority', models.CharField(choices=[('LOW', 'Faible'), ('MEDIUM', 'Moyenne'), ('HIGH', 'Elevée')], help_text='Each issue has a priority between: LOW, MEDIUM, HIGH', max_length=6, verbose_name='Issue priority')),
                ('status', models.CharField(choices=[('TODO', 'A faire'), ('DEV', 'En cours'), ('DONE', 'Terminé')], help_text='Each issue has a tag between: TODO, DEV, DONE', max_length=4, verbose_name='Issue status')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, help_text='issue creation date is automatically filled in.', verbose_name='Created datetime issue')),
                ('assignee_user_id', models.ForeignKey(default=models.ForeignKey(help_text='Each issue has an author. A custom user can have several             issues', on_delete=django.db.models.deletion.CASCADE, related_name='issues', to=settings.AUTH_USER_MODEL, verbose_name='author issue'), help_text='Each issue has an assignee. By default asssignee is the             author', on_delete=django.db.models.deletion.CASCADE, related_name='issues_assign', to=settings.AUTH_USER_MODEL, verbose_name='assignee issue')),
                ('author_user_id', models.ForeignKey(help_text='Each issue has an author. A custom user can have several             issues', on_delete=django.db.models.deletion.CASCADE, related_name='issues', to=settings.AUTH_USER_MODEL, verbose_name='author issue')),
                ('project_id', models.ForeignKey(help_text='Each issue has a project. A project can have several             issues', on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='issuetracking.project', verbose_name='project issue')),
            ],
            options={
                'ordering': ['created_datetime'],
            },
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.CharField(choices=[('CONTRIB', 'Contributeur'), ('AUTHOR', 'Auteur')], help_text="A simple contributor can read everything on project,             issues, comments, he can create issues and commetns but he can't                 delete or update project, issues or comments. An author can                     Update and delete everything he created.", max_length=7, verbose_name='Contributor permission')),
                ('role', models.CharField(help_text=' ', max_length=255, verbose_name='Contributor role')),
                ('project_id', models.ForeignKey(help_text='Each project has sevaral contributors. One of them is the             project author (permission).', on_delete=django.db.models.deletion.CASCADE, to='issuetracking.project', verbose_name='related projects')),
                ('user_id', models.ForeignKey(help_text='Each contributor is a custom user. A user can contribute             to several projects. A user can be a simple contributor or the                 project author', on_delete=django.db.models.deletion.CASCADE, related_name='contributors', to=settings.AUTH_USER_MODEL, verbose_name='related user (project contributor or author)')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='Each comment has a description.', max_length=2048, verbose_name='Comment description')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, help_text='comment creation date is automatically filled in.', verbose_name='Created datetime comments')),
                ('author_user_id', models.ForeignKey(help_text='Each comment has an author. A custom user can have several             comments', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='author comment')),
                ('issue_id', models.ForeignKey(help_text='Each comment has an issue. An issue can have several             comments', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='issuetracking.issue', verbose_name='issue comment')),
            ],
            options={
                'ordering': ['created_datetime'],
            },
        ),
    ]
