from django.core.management.base import BaseCommand

from products.models import Category, Product


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--keep_categories', action='store_true')

    def handle(self, *args, **options):
        Product.objects.all().delete()
        if not options['keep_categories']:
            Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted tree nodes.'))
