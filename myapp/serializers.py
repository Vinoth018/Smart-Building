from rest_framework import serializers
from .models import MyUser, Location, Tenant, Building, Sensor, Incident, Notification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = MyUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            role=validated_data['role'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['location_id', 'country', 'city', 'status']

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['tenant_id', 'name', 'status', 'admin_id']

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ['building_id', 'name', 'address', 'floors', 'location_id', 'status', 'tenant_id', 'description', 'cover_image', 'profile_image', 'zip_code', 'created_date']
        read_only_fields = ['created_date']

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['sensor_id', 'type', 'ip_address', 'room_id', 'building_id', 'status']

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = ['incident_id', 'description', 'status', 'assigned_to', 'due_date', 'resolved_date', 'building_id', 'reported_by']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['notification_id', 'user_id', 'sensor_id', 'building_id', 'message', 'sent_at']
