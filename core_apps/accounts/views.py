from rest_framework.viewsets import ViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserSerializer
)

User = get_user_model()


# Create your views here.
class UserViewSet(ViewSet, ListAPIView, RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
