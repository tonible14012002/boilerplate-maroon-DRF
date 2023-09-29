from rest_framework.viewsets import ModelViewSet
from .models import (
    UserStory,
)
from .serializers import (
    UserStoryDetailSerializer,
)
from .permissions import (
    IsStoryOwner
)
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class UserStoryViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, IsStoryOwner]
    serializer_class = UserStoryDetailSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return UserStory.objects.filter(user=user)

    def get_serializer_context(self):
        return super().get_serializer_context()
