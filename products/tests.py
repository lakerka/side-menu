from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APITestCase

from products.models import Category, Product


class ModelTestCase(TestCase):
    def setUp(self):
        categories = Category.objects
        products = Product.objects
        self.root = categories.create(name='Mineral water')
        self.carbonated = categories.create(name='Carbonated', parent=self.root)
        self.still = categories.create(name='Still', parent=self.root)
        self.vytautas = products.create(name='Vytatutas', price=2, parent=self.carbonated)
        self.birute = products.create(name='Birute', price=2, parent=self.carbonated)
        self.rasa = products.create(name='Rasa', price=2, parent=self.still)

    def test_deleting_root_deletes_all_categories(self):
        self.root.delete()
        category_count = len(Category.objects.all())
        self.assertEquals(category_count, 0)

    def test_deleting_category_deletes_products(self):
        self.carbonated.delete()
        product_count = len(Product.objects.all())
        self.assertEquals(product_count, 1)

    def test_root_parent_path_is_empty(self):
        self.assertEquals(self.root.parent_path, '')

    def test_category_has_correct_parent_path(self):
        expected_path = str(self.root.pk)
        self.assertEquals(self.carbonated.parent_path, expected_path)

    def test_product_has_correct_parent_path(self):
        expected_path = str(self.root.pk) + '.' + str(self.carbonated.pk)
        self.assertEquals(self.birute.parent_path, expected_path)


class ViewTestNormalCase(APITestCase):
    def test_get_tree(self):
        categories = Category.objects
        products = Product.objects
        root = categories.create(name='All')
        books = categories.create(name='Books', parent=root)

        fiction = categories.create(name='Fiction', parent=books)
        drwho = products.create(name='Doctor who.', price=1, parent=fiction)
        timemachine = products.create(name='The time machine.', price=3, parent=fiction)

        history = categories.create(name='History', parent=books)
        coldwar = products.create(name='The cold war.', price=4, parent=history)

        romance = categories.create(name='Romance', parent=books)

        vytautas = products.create(name='Vytautas', price=2, parent=root)

        self.maxDiff = None

        response = self.client.get('/menu/tree')

        expected_tree = {
            'id': root.pk,
            'name': 'All',
            'children': [
                {
                    'id': books.pk,
                    'name': 'Books',
                    'children': [
                        {
                            'id': fiction.pk,
                            'name': 'Fiction',
                            'children': [
                                {
                                    'id': drwho.pk,
                                    'name': 'Doctor who.',
                                    'price': Decimal(1)
                                },
                                {
                                    'id': timemachine.pk,
                                    'name': 'The time machine.',
                                    'price': Decimal(3)
                                }
                            ]
                        },
                        {
                            'id': history.pk,
                            'name': 'History',
                            'children': [
                                {
                                    'id': coldwar.pk,
                                    'name': 'The cold war.',
                                    'price': Decimal(4)
                                }
                            ]
                        },
                        {
                            'id': romance.pk,
                            'name': 'Romance',
                            'children': []
                        }
                    ]
                },
                {
                    'id': vytautas.pk,
                    'name': 'Vytautas',
                    'price': Decimal(2)
                }
            ]
        }
        self.assertEqual(response.data, expected_tree)

    def test_get_tree_with_no_root(self):
        response = self.client.get('/menu/tree')
        expected_tree = None
        self.assertEqual(response.data, expected_tree)

    def test_get_tree_with_no_products(self):
        root = Category.objects.create(name='All')
        books = Category.objects.create(name='Books', parent=root)
        response = self.client.get('/menu/tree')
        expected_tree = {
            'id': root.pk,
            'name': 'All',
            'children': [
                {
                    'id': books.pk,
                    'name': 'Books',
                    'children': []
                }
            ]
        }
        self.assertEqual(response.data, expected_tree)

    def test_get_tree_with_single_category(self):
        root = Category.objects.create(name='All')
        vytautas = Product.objects.create(name='Vytautas', price=1, parent=root)
        birute = Product.objects.create(name='Birute', price=2, parent=root)

        response = self.client.get('/menu/tree')

        expected_tree = {
            'id': root.pk,
            'name': 'All',
            'children': [
                {
                    'id': vytautas.pk,
                    'name': 'Vytautas',
                    'price': Decimal(1)
                },
                {
                    'id': birute.pk,
                    'name': 'Birute',
                    'price': Decimal(2)
                }
            ]
        }
        self.assertEqual(response.data, expected_tree)
