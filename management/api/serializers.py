from rest_framework.serializers import ModelSerializer

from management.models import Parking, ParkingSpace, Ticket

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