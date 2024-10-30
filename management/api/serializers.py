from rest_framework.serializers import ModelSerializer, SerializerMethodField

from management.models import Parking, ParkingSpace, Ticket, Car

class TicketSerializer(ModelSerializer):

    class Meta:
        model = Ticket
        fields = "__all__"

class ParkingSerializer(ModelSerializer):

    class Meta:
        model = Parking
        fields = "__all__"

    
class ParkingSpaceSerializer(ModelSerializer):

    class Meta:
        model = ParkingSpace
        fields = "__all__"

class CarSerializer(ModelSerializer):

    class Meta:
        model = Car
        fields = "__all__"