from django.db import models


class Group(models.Model):
    subject = models.CharField(max_length=200)
    ratio_of_students = models.IntegerField(default=0)
    main_teacher = models.OneToOneField('teachers.Teacher', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.subject}'

    def number_of_students_in_the_group(self):
        cat = Group.objects.annotate(models.Count('student'))
        result = cat[0].student__count
        return result
    number_of_students_in_the_group.short_description = 'Number of students'
