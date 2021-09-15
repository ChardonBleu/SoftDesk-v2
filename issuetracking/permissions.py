from rest_framework.permissions import SAFE_METHODS, BasePermission

from issuetracking.models import Contributor


class IsAuthorProject(BasePermission):
    message = "Seul l'auteur d'un projet/commentaire \
    peut mettre à jour ou supprimer ce projet/commentaire."
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS :
            return True        
        return obj.author_user_id == request.user


class IsContributorProject(BasePermission):
    message = "Seuls les contributeurs d'un projets peuvent accéder aux \
    problèmes et commentaires de ce projet et en créer de nouveaux."
    
    def has_permission(self, request, view):
        """allow 

        Arguments:
            request {[type]} -- [description]
            view {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        project_id = view.kwargs['project_id']
        is_author = Contributor.objects.filter(
            project_id=project_id, 
            user_id=request.user, 
            permission="AUTHOR").exists()
        is_contrib = Contributor.objects.filter(
            project_id=project_id, 
            user_id=request.user, 
            permission="CONTRIB").exists()
                    
        if request.method in SAFE_METHODS or request.method == 'POST':
            return is_author or is_contrib
        if request.method == 'PUT' or request.method == 'DELETE':
            return is_author or is_contrib

        
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS :
            return True
        if request.method == 'DELETE' or request.method == 'PUT':
            return obj.author_user_id == request.user
