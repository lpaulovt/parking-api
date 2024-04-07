from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from management.models import Parking, ParkingSpace, Ticket
from management.api.serializers import ParkingSerializer, ParkingSpaceSerializer, TicketSerializer

class ParkingViewSet(ModelViewSet):
    serializer_class = ParkingSerializer
    queryset = Parking.objects.all()
    permission_classes = [AllowAny]

class ParkingSpaceViewSet(ModelViewSet):
    serializer_class = ParkingSpaceSerializer
    queryset = ParkingSpace.objects.all()
    permission_classes = [AllowAny]

class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = [AllowAny]

