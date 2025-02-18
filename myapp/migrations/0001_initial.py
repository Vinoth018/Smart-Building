# Generated by Django 4.1.13 on 2024-07-08 09:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('role', models.CharField(choices=[('Super admin', 'Super admin'), ('Admin', 'Admin'), ('User', 'User')], max_length=20)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('building_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('floors', models.IntegerField()),
                ('status', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='cover_images/')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('zip_code', models.CharField(max_length=10)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location_id', models.AutoField(primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('tenant_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=20)),
                ('admin_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('sensor_id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
                ('ip_address', models.CharField(max_length=100)),
                ('room_id', models.IntegerField()),
                ('status', models.CharField(max_length=20)),
                ('building_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.building')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('notification_id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.CharField(max_length=255)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('building_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.building')),
                ('sensor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.sensor')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MyToken',
            fields=[
                ('key', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='custom_auth_token', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('incident_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('status', models.CharField(max_length=20)),
                ('due_date', models.DateField()),
                ('resolved_date', models.DateField(blank=True, null=True)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_incidents', to=settings.AUTH_USER_MODEL)),
                ('building_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.building')),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_incidents', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='building',
            name='location_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.location'),
        ),
        migrations.AddField(
            model_name='building',
            name='tenant_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.tenant'),
        ),
    ]
