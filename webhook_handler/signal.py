from django.contrib.auth.models import User, Group
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import MaintenanceProfile

@receiver(m2m_changed, sender=User.groups.through)
def create_maintenance_profile(sender, instance, action, **kwargs):
    if action == 'post_add':
        # Check if the user is now in the maintenance group
        try:
            maintenance_group = Group.objects.get(name='maintenance')
            if maintenance_group in instance.groups.all():
                # Check if the user already has a maintenance profile
                if not MaintenanceProfile.objects.filter(user=instance).exists():
                    # Create a maintenance profile
                    MaintenanceProfile.objects.create(user=instance)
                    print(f'Maintenance profile created for user: {instance.username}')
        except Group.DoesNotExist:
            # If the group doesn't exist, we skip the profile creation
            print("Maintenance group does not exist.")
