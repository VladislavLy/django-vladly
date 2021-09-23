from django.db.models.signals import post_delete, post_save, pre_save

from groups.models import Group

from .models import Student


def pre_save_signal_student(sender, **kwargs):
    name = kwargs['instance'].name
    surname = kwargs['instance'].surname
    kwargs['instance'].name = str(name).capitalize()
    kwargs['instance'].surname = str(surname).capitalize()


pre_save.connect(pre_save_signal_student, sender=Student)


def post_delete_signal_student(sender, **kwargs):
    try:
        the_id = kwargs['instance'].in_the_group_id
        from groups.models import Group
        group = Group.objects.filter(id=the_id).first()
        amount = group.student_set.all().count()
        group.ratio_of_students = amount
        group.save()
    except AttributeError:
        pass


post_delete.connect(post_delete_signal_student, sender=Student)


data_dict = {}


def post_save_signal_student(sender, **kwargs):
    # print(data_dict)
    # print(kwargs['instance'].in_the_group)
    if kwargs['instance'].name in data_dict.keys():
        try:
            the_id = data_dict.get(kwargs['instance'].name)
            group = Group.objects.filter(id=the_id).first()
            group.ratio_of_students = group.ratio_of_students - 1
            group.save()
            # print(kwargs['instance'].in_the_group)
        except AttributeError:
            pass
    else:
        if kwargs['instance'].in_the_group is not None:
            data_dict[kwargs['instance'].name] = kwargs['instance'].in_the_group_id
            # print(data_dict)

    try:
        the_id = kwargs['instance'].in_the_group_id
        group = Group.objects.filter(id=the_id).first()
        the_var = 0
        if group is None:
            the_var = 1
        else:
            amount = group.student_set.all().count()
            group.ratio_of_students = amount - the_var
            group.save()
            # print(data_dict)
    except AttributeError:
        pass


post_save.connect(post_save_signal_student, sender=Student)
