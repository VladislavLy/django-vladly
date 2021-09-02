from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Group


@receiver(pre_save, sender=Group)
def pre_save_signal_group(sender, **kwargs):
    subject = kwargs['instance'].subject
    kwargs['instance'].subject = str(subject).capitalize()
