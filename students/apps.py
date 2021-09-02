from django.apps import AppConfig


class StudentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'students'

    def ready(self):
        Student = self.get_model('Student')
        from django.db.models.signals import pre_save
        from .signals import pre_save_signal_student

        pre_save.connect(pre_save_signal_student, sender=Student)
