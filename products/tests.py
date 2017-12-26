from django.test import TestCase

from products.models import Category, Product


class ModelDeletionTestCase(TestCase):
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

    def test_deleting_ancestor_category_deletes_products(self):
        self.carbonated.delete()
        product_count = len(Product.objects.all())
        self.assertEquals(product_count, 1)
