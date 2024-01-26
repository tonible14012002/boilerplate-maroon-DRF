from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from rest_framework.generics import CreateAPIView

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
