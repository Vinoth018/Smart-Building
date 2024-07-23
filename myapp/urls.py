# from django.urls import path
# from .views import RegisterView, LoginView, LocationListCreateView, LocationDetailView, TenantListCreateView, TenantDetailView, BuildingListCreateView, BuildingDetailView, SensorListCreateView, SensorDetailView, IncidentListCreateView, IncidentDetailView, NotificationListCreateView, NotificationDetailView

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('locations/', LocationListCreateView.as_view(), name='location-list-create'),
#     path('locations/<int:pk>/', LocationDetailView.as_view(), name='location-detail'),
#     path('tenants/', TenantListCreateView.as_view(), name='tenant-list-create'),
#     path('tenants/<int:pk>/', TenantDetailView.as_view(), name='tenant-detail'),
#     path('buildings/', BuildingListCreateView.as_view(), name='building-list-create'),
#     path('buildings/<int:pk>/', BuildingDetailView.as_view(), name='building-detail'),
#     path('sensors/', SensorListCreateView.as_view(), name='sensor-list-create'),
#     path('sensors/<int:pk>/', SensorDetailView.as_view(), name='sensor-detail'),
#     path('incidents/', IncidentListCreateView.as_view(), name='incident-list-create'),
#     path('incidents/<int:pk>/', IncidentDetailView.as_view(), name='incident-detail'),
#     path('notifications/', NotificationListCreateView.as_view(), name='notification-list-create'),
#     path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
# ]






# myapp.urls.py
from django.urls import path
from .views import RegisterView, LoginView, LocationListCreateView, LocationDetailView, TenantListCreateView, TenantDetailView, BuildingListCreateView, BuildingDetailView, SensorListCreateView, SensorDetailView, IncidentListCreateView, IncidentDetailView, NotificationListCreateView, NotificationDetailView, UserDataView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('locations/', LocationListCreateView.as_view(), name='location-list-create'),
    path('locations/<int:pk>/', LocationDetailView.as_view(), name='location-detail'),
    path('tenants/', TenantListCreateView.as_view(), name='tenant-list-create'),
    path('tenants/<int:pk>/', TenantDetailView.as_view(), name='tenant-detail'),
    path('buildings/', BuildingListCreateView.as_view(), name='building-list-create'),
    path('buildings/<int:pk>/', BuildingDetailView.as_view(), name='building-detail'),
    path('sensors/', SensorListCreateView.as_view(), name='sensor-list-create'),
    path('sensors/<int:pk>/', SensorDetailView.as_view(), name='sensor-detail'),
    path('incidents/', IncidentListCreateView.as_view(), name='incident-list-create'),
    path('incidents/<int:pk>/', IncidentDetailView.as_view(), name='incident-detail'),
    path('notifications/', NotificationListCreateView.as_view(), name='notification-list-create'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('user-data/<int:user_id>/', UserDataView.as_view(), name='user-data'),
]
