from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.IntegerField(default=18)
    subject_class = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} {self.surname}'


ALL_SUBGECTS = ('Information Systems & Computer science',
                'Music', 'Engineering', 'Business & Management',
                'Arts & Design', 'Law', 'Medicine', 'Language & Literature',
                'Architecture', 'Accounting & Finance', 'Mathematics', 'History', 'Chemistry',
                'Physics', 'Biology', 'Performing Arts & Acting', 'Psychology')
