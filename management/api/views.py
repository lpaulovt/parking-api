from datetime import datetime
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotAuthenticated, PermissionDenied

from core.permissions import IsManager, IsEmployee
from management.models import Parking, ParkingSpace, Ticket
from management.api.serializers import ParkingSerializer, ParkingSpaceSerializer, TicketSerializer
from management.services import ParkingService, ParkingSpaceService, TicketService

class ParkingViewSet(ModelViewSet):
    serializer_class = ParkingSerializer
    queryset = Parking.objects.all()
    permission_classes = [IsManager]
    service = ParkingService()

    def create(self, request, *args, **kwargs):
        serializer = ParkingSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            new_parking = self.service.create(serializer, request.user)
            serializer = ParkingSerializer(new_parking)
            return Response(
                {"Info": "Parking created!", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except (ParseError, ValueError):
            return Response(
                {
                    "Info": "Fail to create new parking!"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except PermissionDenied:
            return Response(
                {"Info": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN
            )
        except NotAuthenticated:
            return Response(
                {"Info": "Not Authenticated User."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

class ParkingSpaceViewSet(ModelViewSet):
    serializer_class = ParkingSpaceSerializer
    queryset = ParkingSpace.objects.all()
    permission_classes = [IsEmployee | IsManager]
    service = ParkingSpaceService()

    def create(self, request, *args, **kwargs):
        serializer = ParkingSpaceSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            new_parking_space = self.service.create(serializer, request.user)
            serializer = ParkingSpaceSerializer(new_parking_space)
            return Response(
                {"Info": "Parking space created!", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except (ParseError, ValueError):
            return Response(
                {
                    "Info": "Fail to create new parking space!"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except PermissionDenied:
            return Response(
                {"Info": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN
            )
        except NotAuthenticated:
            return Response(
                {"Info": "Not Authenticated User."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = [IsEmployee | IsManager]
    service = TicketService()

    def create(self, request, *args, **kwargs):
        serializer = TicketSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            new_ticket = self.service.create(serializer, request.user)
            serializer = TicketSerializer(new_ticket)
            return Response(
                {"Info": "Ticket created!", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except (ParseError, ValueError):
            return Response(
                {
                    "Info": "Fail to create new ticket!"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except PermissionDenied:
            return Response(
                {"Info": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN
            )
        except NotAuthenticated:
            return Response(
                {"Info": "Not Authenticated User."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    @action(methods=['get'],detail=True, url_path="payment")
    def calculateTicket(self, request, pk):
        try:
            ticket = self.get_object()
            updated_ticket = self.service.calc_ticket(ticket)
            serializer = TicketSerializer(updated_ticket)
            return Response(
                {"Info": "Ticket checkout!", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Ticket.DoesNotExist:
            return Response(
                {
                    "Info": "Fail to calculate Ticket!"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except NotAuthenticated:
            return Response(
                {"Info": "Not Authenticated User."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except PermissionDenied:
            return Response(
                {"Info": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN
            )