from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Teacher


@receiver(pre_save, sender=Teacher)
def pre_save_signal_teacher(sender, **kwargs):
    name = kwargs['instance'].name
    surname = kwargs['instance'].surname
    subject_class = kwargs['instance'].subject_class
    kwargs['instance'].subject_class = str(subject_class).capitalize()
    kwargs['instance'].name = str(name).capitalize()
    kwargs['instance'].surname = str(surname).capitalize()
