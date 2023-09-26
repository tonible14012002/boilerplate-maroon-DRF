from rest_framework.viewsets import ViewSet
from rest_framework.generics import (
    RetrieveAPIView,
    UpdateAPIView,
    ListAPIView,
    CreateAPIView,
)
from .serializers import (
    UserProfileSerializer,
    UserRegistrationSerializer,
    ProfileSerializer
)
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.
class ProfileViewSet(ViewSet, ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserProfileViewset(ViewSet, RetrieveAPIView, UpdateAPIView, ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'id'


class ProfileRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
