from django.db.models.signals import pre_save

from .models import Student


def pre_save_signal_student(sender, **kwargs):
    name = kwargs['instance'].name
    surname = kwargs['instance'].surname
    kwargs['instance'].name = str(name).capitalize()
    kwargs['instance'].surname = str(surname).capitalize()


pre_save.connect(pre_save_signal_student, sender=Student)
