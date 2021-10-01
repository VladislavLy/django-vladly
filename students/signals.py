from django.db.models.signals import post_delete, pre_save

from groups.models import Group

from .models import Student


def pre_save_signal_student(sender, **kwargs):
    if not Student.objects.filter(id=kwargs['instance'].id):
        if kwargs['instance'].in_the_group:
            group_id_go_to = kwargs['instance'].in_the_group.id
            group_go = Group.objects.filter(id=group_id_go_to).first()
            group_go.ratio_of_students = group_go.ratio_of_students + 1
            group_go.save()
        else:
            pass

    elif Student.objects.get(id=kwargs['instance'].id).in_the_group is None:
        try:
            group_id_go_to = kwargs['instance'].in_the_group.id
            group_go = Group.objects.filter(id=group_id_go_to).first()
            group_go.ratio_of_students = group_go.ratio_of_students + 1
            group_go.save()
        except AttributeError:
            pass

    elif kwargs['instance'].in_the_group is None:
        group_id_from_where = Student.objects.get(id=kwargs['instance'].id).in_the_group.id
        group_from = Group.objects.filter(id=group_id_from_where).first()
        group_from.ratio_of_students = group_from.ratio_of_students - 1
        group_from.save()

    else:
        group_id_go_to = kwargs['instance'].in_the_group.id
        group_id_from_where = Student.objects.get(id=kwargs['instance'].id).in_the_group.id
        group_go = Group.objects.filter(id=group_id_go_to).first()
        group_go.ratio_of_students = group_go.ratio_of_students + 1
        group_go.save()
        group_from = Group.objects.filter(id=group_id_from_where).first()
        group_from.ratio_of_students = group_from.ratio_of_students - 1
        group_from.save()

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
