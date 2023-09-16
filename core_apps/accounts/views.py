from rest_framework.viewsets import ViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer
)

User = get_user_model()


# Create your views here.
class UserViewSet(ViewSet, ListAPIView, RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
