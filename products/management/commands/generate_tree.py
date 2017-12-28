import argparse
import random
import string
import decimal
from functools import partial

from django.core.management.base import BaseCommand

from products.models import Category, Product


def int_greater_than(value, greater_than=None):
    ivalue = int(value)
    if greater_than is not None and ivalue <= greater_than:
        raise argparse.ArgumentTypeError("Expected integer greater than %s but got: %s" % (greater_than, value))
    return ivalue


def get_random_price():
    return decimal.Decimal(random.randrange(101, 909)) / 100


def get_random_is_active():
    return random.choice([True, True, False])


def get_random_name():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))


def get_category(parent=None):
    name = 'Category ' + get_random_name()
    is_active = get_random_is_active()
    category = Category.objects.create(name=name, active=is_active, parent=parent)
    return category


def get_product(parent=None):
    name = 'Product ' + get_random_name()
    is_active = get_random_is_active()
    price = get_random_price()
    product = Product.objects.create(name=name, active=is_active, price=price, parent=parent)
    return product


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('category_count', type=partial(int_greater_than, greater_than=0))
        parser.add_argument('product_count', type=partial(int_greater_than, greater_than=0))
        parser.add_argument('max_level', type=partial(int_greater_than, greater_than=1))

    def handle(self, *args, **options):
        category_count = options['category_count']
        product_count = options['product_count']
        max_level = options['max_level']

        categories = [(1, get_category(parent=None))]
        for i in range(1, category_count):
            right_level_categories = list(filter(lambda pair: pair[0] < max_level, categories))
            parent_level, parent_category = random.choice(right_level_categories)
            category = get_category(parent=parent_category)
            categories.append((parent_level + 1, category))

        products = []
        right_level_categories = list(filter(lambda pair: pair[0] < max_level, categories))
        for i in range(0, product_count):
            _, category = random.choice(right_level_categories)
            product = get_product(parent=category)
            products.append(product)

        self.stdout.write(self.style.SUCCESS('Successfully generated tree.'))
