from django.core.management.base import BaseCommand

from faker import Faker

from teachers.models import Teacher


class Command(BaseCommand):
    help = 'Generate random teachers based on input amount' # noqa

    def add_arguments(self, parser):
        parser.add_argument('number_of_teachers', nargs='?', type=int)

    def handle(self, *args, **options):
        fake = Faker()
        result = []
        Teacher.objects.all().delete()

        if options['number_of_teachers'] is not None:
            pass
        else:
            options['number_of_teachers'] = 100

        for i in range(options['number_of_teachers']):
            result.append(Teacher(
                name=fake.first_name(),
                surname=fake.last_name(),
                age=fake.random.randint(19, 70),))

        Teacher.objects.bulk_create(result)
        self.stdout.write(self.style.SUCCESS('Successfully created teachers ✔ '))
