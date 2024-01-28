from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from . import models
from core_apps.user import models as user_models

# Create your views here.
# APIView provide as_view() method for converting class-based views into function-based views.
# request.user is the user instance of the current user
# Serializer
# - Input data -> validate data -> create Instance base on validated data
# - Input instance -> serialize instance in to Python native data type (dictionary) -> return data


class CreateHouseView(CreateAPIView):
    # def get(self, request):
    #     return Response({'status': 'get ok'})

    # def post(self, request):
    #     # Create house instance in database
    #     return Response({'status': 'ok'})
    serializer_class = serializers.HouseDetailSerializer

class ListHouseView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.HouseDetailSerializer
    def get_queryset(self):
        return models.House.objects.filter(owner=self.request.user)

class UpdateHouseView(UpdateAPIView):
    # queryset = models.House.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UpdateHouseSerializer
    # lookup_field = 'id'

    def get_object(self):
        user = self.request.user
        house_id = self.kwargs['id']
        return models.House.objects.filter(owner=user, id=house_id).first()

class DeleteHouseView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.DeleteHouseSerializer
    
    def get_object(self):
        user = self.request.user
        house_id = self.kwargs['id']
        return models.House.objects.filter(owner=user, id=house_id).first()

class AddUserToHouseView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.HouseDetailSerializer
    
    def post(self, request, id, phone_number):
        house = models.House.objects.filter(owner=request.user, id=id).first()
        if house is None:
            return Response({'status': 'House not found'})
        user = user_models.MyUser.objects.filter(phone=phone_number).first()
        if user is None:
            return Response({'status': 'User not found'})
        house.owner.add(user)
        house.save()
        serializer = self.get_serializer(house)
        return Response(serializer.data)