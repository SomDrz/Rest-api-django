from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    reset_password_token = models.CharField(max_length=50, default='', blank=True)
    reset_password_expire = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_or_save_profile(sender, instance, created, **kwargs):
    """
    Signal to create or save a Profile object when a User is created or updated.
    """
    if created:
        # Create a new profile for the user
        Profile.objects.create(user=instance)
    else:
        # Save the profile when the user is updated
        instance.profile.save()
