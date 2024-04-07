from datetime import datetime
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response


from core.permissions import IsManager, IsEmployee
from management.models import Parking, ParkingSpace, Ticket
from management.api.serializers import ParkingSerializer, ParkingSpaceSerializer, TicketSerializer

class ParkingViewSet(ModelViewSet):
    serializer_class = ParkingSerializer
    queryset = Parking.objects.all()
    permission_classes = [IsManager]

class ParkingSpaceViewSet(ModelViewSet):
    serializer_class = ParkingSpaceSerializer
    queryset = ParkingSpace.objects.all()
    permission_classes = [IsEmployee, IsManager]

class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = [IsEmployee, IsManager]

    @action(methods=['get'],detail=True, url_path="payment" )
    def calculateTicket(self, request, pk):
        ticket = self.get_object()
        reference_date = datetime.now().date()

        combined_checkin = datetime.combine(reference_date, ticket.checkin)
        combined_checkout = datetime.combine(reference_date, ticket.checkout)
        
        total_time = combined_checkout - combined_checkin
        ticket.value = total_time.total_seconds() / 3600 *ticket.parking_space.parking.hour_price
        ticket.save()
        serializer = TicketSerializer(ticket)
        return Response(
            {"Info": "Ticket checkout!", "data": serializer.data},
            status=status.HTTP_200_OK,
        )
 