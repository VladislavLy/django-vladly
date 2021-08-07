from django.db import models


class Group(models.Model):
	subject = models.CharField(max_length=200)
	ratio_of_students = models.IntegerField(default=12)

	def __str__(self):
		return '%s, %s, %s' % (self.id, self.subject, self.ratio_of_students)
