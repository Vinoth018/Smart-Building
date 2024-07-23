# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.contrib.auth import authenticate
# from .models import MyUser, MyToken, Location, Tenant, Building, Sensor, Incident, Notification
# from .serializers import UserSerializer, LoginSerializer, LocationSerializer, TenantSerializer, BuildingSerializer, SensorSerializer, IncidentSerializer, NotificationSerializer

# class RegisterView(generics.CreateAPIView):
#     queryset = MyUser.objects.all()
#     serializer_class = UserSerializer

# class LoginView(APIView):
#     serializer_class = LoginSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data['email']
#         password = serializer.validated_data['password']
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             token, created = MyToken.objects.get_or_create(user=user)
#             return Response({'token': token.key}, status=status.HTTP_200_OK)
#         return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# class LocationListCreateView(generics.ListCreateAPIView):
#     queryset = Location.objects.all()
#     serializer_class = LocationSerializer

# class LocationDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Location.objects.all()
#     serializer_class = LocationSerializer

# class TenantListCreateView(generics.ListCreateAPIView):
#     queryset = Tenant.objects.all()
#     serializer_class = TenantSerializer

# class TenantDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Tenant.objects.all()
#     serializer_class = TenantSerializer

# class BuildingListCreateView(generics.ListCreateAPIView):
#     queryset = Building.objects.all()
#     serializer_class = BuildingSerializer

# class BuildingDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Building.objects.all()
#     serializer_class = BuildingSerializer

# class SensorListCreateView(generics.ListCreateAPIView):
#     queryset = Sensor.objects.all()
#     serializer_class = SensorSerializer

# class SensorDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Sensor.objects.all()
#     serializer_class = SensorSerializer

# class IncidentListCreateView(generics.ListCreateAPIView):
#     queryset = Incident.objects.all()
#     serializer_class = IncidentSerializer

# class IncidentDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Incident.objects.all()
#     serializer_class = IncidentSerializer

# class NotificationListCreateView(generics.ListCreateAPIView):
#     queryset = Notification.objects.all()
#     serializer_class = NotificationSerializer

# class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Notification.objects.all()
#     serializer_class = NotificationSerializer



# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .models import MyUser, Location, Tenant, Building, Sensor, Incident, Notification
from .serializers import UserSerializer, LoginSerializer, LocationSerializer, TenantSerializer, BuildingSerializer, SensorSerializer, IncidentSerializer, NotificationSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['role'] = self.user.role
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class LoginView(CustomTokenObtainPairView):
    pass

class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class TenantListCreateView(generics.ListCreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

class TenantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

class BuildingListCreateView(generics.ListCreateAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

class BuildingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

class SensorListCreateView(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class SensorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class IncidentListCreateView(generics.ListCreateAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

class IncidentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class UserDataView(APIView):
    def get(self, request, user_id):
        try:
            user = MyUser.objects.get(id=user_id)
        except MyUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user_data = UserSerializer(user).data

        # Fetch related data
        tenants = Tenant.objects.filter(admin_id=user)
        buildings = Building.objects.filter(tenant_id__in=tenants)
        locations = Location.objects.filter(location_id__in=buildings.values('location_id'))
        sensors = Sensor.objects.filter(building_id__in=buildings)
        incidents_reported = Incident.objects.filter(reported_by=user)
        incidents_assigned = Incident.objects.filter(assigned_to=user)
        notifications = Notification.objects.filter(user_id=user)

        # Serialize related data
        user_data['tenants'] = TenantSerializer(tenants, many=True).data
        user_data['locations'] = LocationSerializer(locations, many=True).data
        user_data['buildings'] = BuildingSerializer(buildings, many=True).data
        user_data['sensors'] = SensorSerializer(sensors, many=True).data
        user_data['incidents_reported'] = IncidentSerializer(incidents_reported, many=True).data
        user_data['incidents_assigned'] = IncidentSerializer(incidents_assigned, many=True).data
        user_data['notifications'] = NotificationSerializer(notifications, many=True).data

        return Response(user_data, status=status.HTTP_200_OK)