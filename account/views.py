from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from account.models import User
from account.serializers import UserSerializer


class UserSignUpView(generics.CreateAPIView):
    """
    This endpoint can be used to signup on  the **SoftDesk API**.

    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
