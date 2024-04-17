from datetime import datetime
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotAuthenticated, PermissionDenied

from core.permissions import IsManager, IsEmployee
from management.models import Parking, ParkingSpace, Ticket
from management.api.serializers import ParkingSerializer, ParkingSpaceSerializer, TicketSerializer

class ParkingViewSet(ModelViewSet):
    serializer_class = ParkingSerializer
    queryset = Parking.objects.all()
    permission_classes = [IsManager]

    def create(self, request, *args, **kwargs):
        serializer = ParkingSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            new_parking = Parking.objects.create(
                parking_name = serializer.validated_data['parking_name'],
                hour_price = serializer.validated_data['hour_price'],
                created_by = request.user,
            )
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

    def create(self, request, *args, **kwargs):
        serializer = ParkingSpaceSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            new_parking_space = ParkingSpace.objects.create(
                cod = serializer.validated_data['cod'],
                status = serializer.validated_data['status'],
                parking = serializer.validated_data['parking'],
                created_by = request.user,
            )
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

    def create(self, request, *args, **kwargs):
        serializer = TicketSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            new_parking_space = Ticket.objects.create(
                model = serializer.validated_data['model'],
                license_plate = serializer.validated_data['license_plate'],
                checkin = serializer.validated_data['checkin'],
                checkout = serializer.validated_data['checkout'],
                parking_space = serializer.validated_data['parking_space'],
                value = serializer.validated_data['value'],
                created_by = request.user,
            )
            serializer = TicketSerializer(new_parking_space)
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