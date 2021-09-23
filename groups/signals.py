from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Group


@receiver(pre_save, sender=Group)
def pre_save_signal_group(sender, **kwargs):
    # print(kwargs['instance'].student_set.all())
    # the_id = kwargs['instance'].id
    # print(the_id)
    # id_groups = []
    # for gr in Group.objects.all():
    #     id_groups.append({gr.id: 0})
    # for st in Student.objects.all():
    #     pass
    #     for k in id_groups:
    #         pass
    #         a = st.in_the_group_id
    #         if st.in_the_group_id in k.keys():
    #             k.update({a: 1+ k[a]})
    #             k[a]
    # print(id_groups)
    # count = [i for i in id_groups if the_id in i.keys()]
    # print(count[0].get(the_id))
    # kwargs['instance'].ratio_of_students = int(count[0].get(the_id))
    # from django.db import models
    # cat = Group.objects.annotate(models.Count('student'))
    # print(cat.__dict__)
    # print(cat[1].student__count)
    # kwargs['instance'].ratio_of_students =
    subject = kwargs['instance'].subject
    kwargs['instance'].subject = str(subject).capitalize()


# @receiver(post_save, sender=Group)
# def post_save_signal_group(sender, **kwargs):
#     from students.models import Student
#     print(kwargs['instance'].id)
#     from django.db import models
#     cat = Group.objects.annotate(models.Count('student'))
#     print(cat[0].student__count)
#     kwargs['instance'].ratio_of_students = cat[0].student__count


def post_delete_signal_teacher(sender, **kwargs):
    try:
        the_id = kwargs['instance'].main_teacher_id
        from teachers.models import Teacher
        teacher = Teacher.objects.filter(id=the_id).first()
        teacher.subject_class = '-empty-'
        teacher.save()
    except AttributeError:
        pass


post_delete.connect(post_delete_signal_teacher, sender=Group)
