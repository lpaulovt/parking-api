from datetime import datetime
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotAuthenticated, PermissionDenied

from core.permissions import IsManager, IsEmployee
from management.models import Parking, ParkingSpace, Ticket, Car
from management.api.serializers import ParkingSerializer, ParkingSpaceSerializer, TicketSerializer, CarSerializer
from management.services import ParkingService, ParkingSpaceService, TicketService

class ParkingViewSet(ModelViewSet):
    serializer_class = ParkingSerializer
    queryset = Parking.objects.all()
    service = ParkingService()
    # permission_classes = [IsManager]

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

    def list(self, request, *args, **kwargs):
        try:
            user_id = request.query_params.get('id')

            if user_id:
                queryset = self.get_queryset().filter(user=user_id)
                if not queryset.exists():
                    return Response(
                        {"Info": "No parking records found for this user.",  "data": []},
                        status=status.HTTP_200_OK,
                    )
            else:
                queryset = self.get_queryset()

            serializer = ParkingSerializer(queryset, many=True)
            return Response(
                {"Info": "Parking records", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        except NotAuthenticated:
            return Response(
                {"Info": "Not Authenticated User."}, status=status.HTTP_401_UNAUTHORIZED
            )
        except PermissionDenied:
            return Response(
                {"Info": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN
            )
class ParkingSpaceViewSet(ModelViewSet):
    serializer_class = ParkingSpaceSerializer
    queryset = ParkingSpace.objects.all()
    service = ParkingSpaceService()
    # permission_classes = [IsEmployee, IsManager]

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
    service = TicketService()
    #permission_classes = [IsEmployee, IsManager]

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
        
class CarViewSet(ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    #permission_classes = [IsEmployee, IsManager]

    def create(self, request, *args, **kwargs):
        serializer = CarSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            new_car = Car.objects.create(
                model = serializer.validated_data['model'],
                license_plate = serializer.validated_data['license_plate'],
                user = serializer.validated_data['user'],
                created_by = request.user,
            )
            serializer = CarSerializer(new_car)
            return Response(
                {"Info": "Car list", "data": serializer.data},
                status=status.HTTP_200_OK,
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
        
    def filterByUser(self, request, id=None, *args, **kwargs):
        try:
            queryset = super().get_queryset()
            if customer_id is not None:
                queryset = queryset.filter(user=id)
            return queryset
            serializer = CarSerializer(ticket)
            return Response(
                {"Info": "Car", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Ticket.DoesNotExist:
            return Response(
                {
                    "Info": "Fail find cars"
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
