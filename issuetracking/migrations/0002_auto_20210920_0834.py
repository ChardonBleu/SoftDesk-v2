# Generated by Django 3.2.7 on 2021-09-20 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issuetracking', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='author_user_id',
            new_name='author_user',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='issue_id',
            new_name='issue',
        ),
        migrations.RenameField(
            model_name='contributor',
            old_name='project_id',
            new_name='project',
        ),
        migrations.RenameField(
            model_name='contributor',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='issue',
            old_name='assignee_user_id',
            new_name='assignee_user',
        ),
        migrations.RenameField(
            model_name='issue',
            old_name='author_user_id',
            new_name='author_user',
        ),
        migrations.RenameField(
            model_name='issue',
            old_name='project_id',
            new_name='project',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='author_user_id',
            new_name='author_user',
        ),
    ]