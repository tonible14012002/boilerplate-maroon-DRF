from rest_framework.viewsets import ViewSet
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView
)
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer
)

User = get_user_model()


# Create your views here.
class UserViewSet(ViewSet, ListAPIView, RetrieveAPIView, CreateAPIView):
    queryset = User.objects.all()
    lookup_field = "id"

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserRegistrationSerializer
        return UserSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return []
        return [IsAuthenticated()]
