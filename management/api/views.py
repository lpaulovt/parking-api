from datetime import datetime
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotAuthenticated, PermissionDenied



from core.permissions import IsManager, IsEmployee
from management.models import Parking, ParkingSpace, Ticket, Car
from management.api.serializers import ParkingSerializer, ParkingSpaceSerializer, TicketSerializer, CarSerializer

class ParkingViewSet(ModelViewSet):
    serializer_class = ParkingSerializer
    queryset = Parking.objects.all()
    # permission_classes = [IsManager]

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
    # permission_classes = [IsEmployee, IsManager]

    def create(self, request, *args, **kwargs):
        serializer = ParkingSpaceSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            new_parking_space = ParkingSpace.objects.create(
                cod = serializer.validated_data['cod'],
                status = serializer.validated_data['status'],
                parking = serializer.validated_data['parking'],
                pwd = serializer.validated_data['pwd'],
                created_by = request.user,
            )
            serializer = ParkingSpaceSerializer(new_parking_space)
            return Response(
                {"Info": "Parking space created!", "data": serializer.data},
                status=status.HTTP_200_OK,
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
    #permission_classes = [IsEmployee, IsManager]

    def create(self, request, *args, **kwargs):
        serializer = TicketSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            new_parking_space = Ticket.objects.create(
                checkin = serializer.validated_data['checkin'],
                checkout = serializer.validated_data['checkout'],
                car = serializer.validated_data['car'],
                parking_space = serializer.validated_data['parking_space'],
                value = serializer.validated_data['value'],
                created_by = request.user,
            )
            serializer = TicketSerializer(new_parking_space)
            return Response(
                {"Info": "Ticket created!", "data": serializer.data},
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

    @action(methods=['get'],detail=True, url_path="payment" )
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
        
class CarViewSet(ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    #permission_classes = [IsEmployee, IsManager]