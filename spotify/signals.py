from django.db.models.signals import post_save
from django.dispatch import receiver


from .models import *


@receiver(post_save, sender=UserSubscription)
def update_profile_subscription(sender, instance, created, **kwargs):
    if not created:
        return
    instance.user.profile.extend_premium_until(instance.subscription.duration)
