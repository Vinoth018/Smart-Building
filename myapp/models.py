from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, role, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            role=role,
        )
        user.set_password(password)

        if role == 'Super admin':
            user.is_superuser = True
            user.is_admin = True
        elif role == 'Admin':
            user.is_superuser = False
            user.is_admin = True
        else:  
            user.is_superuser = False
            user.is_admin = False

        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        return self.create_user(
            email,
            username=username,
            role='Super admin',
            password=password
        )

class MyUser(AbstractBaseUser):
    ROLE_CHOICES = [
        ('Super admin', 'Super admin'),
        ('Admin', 'Admin'),
        ('User', 'User'),
    ]
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    username = models.CharField(max_length=30, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class MyToken(models.Model):
    key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='custom_auth_token', 
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):                    
        return str(self.key)

class Location(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    location_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"{self.city}, {self.country} ({self.status})"

class Tenant(models.Model):
    tenant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    admin_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)

class Building(models.Model):
    building_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    floors = models.IntegerField()
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='cover_images/', null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    zip_code = models.CharField(max_length=10)
    created_date = models.DateTimeField(auto_now_add=True)

class Sensor(models.Model):
    sensor_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)
    room_id = models.IntegerField() 
    building_id = models.ForeignKey(Building, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    
class Incident(models.Model):
    incident_id = models.AutoField(primary_key=True)
    description = models.TextField()
    status = models.CharField(max_length=20)
    assigned_to = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='assigned_incidents')
    due_date = models.DateField()
    resolved_date = models.DateField(null=True, blank=True)
    building_id = models.ForeignKey(Building, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='reported_incidents')

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    building_id = models.ForeignKey(Building, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    sent_at = models.DateTimeField(auto_now_add=True)
