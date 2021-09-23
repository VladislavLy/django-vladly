from django.core.management.base import BaseCommand

from faker import Faker

from groups.models import Group

from students.models import Student

from teachers.models import ALL_SUBGECTS, Teacher


class Command(BaseCommand):
    help = 'Generate random teachers based on input amount' # noqa

    def add_arguments(self, parser):
        parser.add_argument('number_of_teachers', nargs='?', type=int)

    def handle(self, *args, **options):
        fake = Faker()
        Teacher.objects.all().delete()
        Student.objects.all().delete()
        Group.objects.all().delete()

        if options['number_of_teachers'] is not None:
            pass
        else:
            options['number_of_teachers'] = 1

        for i in range(options['number_of_teachers']):

            teach = Teacher(name=fake.first_name(),
                            surname=fake.last_name(),
                            age=fake.random_int(20, 70),
                            subject_class=fake.random.choice(ALL_SUBGECTS)
                            )
            teach.save()

            gr = Group(subject=teach.subject_class,
                       ratio_of_students=fake.random.randint(1, 8),
                       main_teacher=teach,
                       )
            gr.save()

            for i in range(gr.ratio_of_students):
                st = Student(name=fake.first_name(),
                             surname=fake.last_name(),
                             age=fake.random_int(18, 40),
                             phone=fake.msisdn(),
                             in_the_group=gr,
                             )
                st.save()

        self.stdout.write(self.style.SUCCESS('Successfully created teachers ✔ '))
